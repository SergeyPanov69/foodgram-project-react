# from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile

# from django.contrib.auth.hashers import check_password
from djoser.serializers import (SetPasswordSerializer,
                                UserSerializer, UserCreateSerializer)
from rest_framework import serializers, status
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Favorite, Ingredient, IngredientQuantity, Recipe, Shopping, Tag
# from users.validators import validate_username
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from users.validators import validate_tags #, validate_ingredients

# User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientQuantitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientQuantity
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для моделт Recipe.
    Укороченный набор полей"""
    image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time'),
        read_only_fields = ('__all__', )


class SubscribeSerializer(CustomUserSerializer):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.ReadOnlyField(
        source='author.recipe.count')

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = ('__all__', )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    ingredients = IngredientQuantitySerializer(
        many=True, source='ingredientamount_set'
    )
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author','description','tags','ingredients',
            'image', 'cooking_time', 'is_favorited', 'is_in_shopping_cart',
        )
        read_only_fields = ('ingredients', 'author', 'tags', 'is_favorite', 'is_shopping_card',)

    def get_is_favorite(self, obj) -> bool:
        """Находится ли рецепт в списке любимых.
        True - если рецепт в любимых у запрашевающего пользователя.
        False - не находится или пользователь не авторизован.
        """
        request = self.context.get('request') #.request.user
        # if user.is_anonymous:
        if not request.user.is_authenticated:
            return False
        # return Subscription.objects.filter(recipe=obj).exists()
        return Favorite.objects.filter(
            user=self.context.get('request').user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Находиться ли рецепт в корзине покупок.
        True - если рецепт в корзине у запрашевающего пользователя.
        False - не находится или пользователь не авторизован.
        """
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Shopping.objects.filter(
            user=self.context.get('request').user,
            recipe=obj
        ).exists()

    def create_tags(self, data, recipe):
        """Создание тега рецепта."""
        valid_tags = validate_tags(data.get('tags'))
        tags = Tag.objects.filter(id_in=valid_tags)
        recipe.tags.set(tags)

    def create(self, validated_data):
        """Создание рецепта."""
        valid_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(self.initial_data, recipe)
        self.create_ingredient_amount(valid_ingredients, recipe)
        return recipe

    # def validate(self, data):
    #     ingredients = self.initial_data.get('ingredients')
    #     valid_ingredients = validate_ingredients(ingredients)
    #     data['ingredients'] = valid_ingredients
    #     return data

    def update(self, instance, validated_data):
        """Изменение рецепта."""
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        instance.tags.remove()
        self.create_tags(self.initial_data, instance)
        instance.ingredientamount_set.filter(recipe__in=[instance.id]).delete()
        valid_ingredients = validated_data.get(
            'ingredients', instance.ingredients)
        self.create_ingredient_amount(valid_ingredients, instance)
        return instance