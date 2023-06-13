from djoser.serializers import (SetPasswordSerializer,
                                UserSerializer, UserCreateSerializer)
from rest_framework import serializers, status
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

# from api.serializers import ShortRecipeSerializer
# from recipes.models import Ingredient, IngredientQuantity, Recipe, Shopping, Favorite, Tag
from users.validators import validate_username
from users.models import Subscription, CustomUser

# User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя.
    Обработка [GET] запроса."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        write_only_fields = ('password',)

    def get_is_subscribed(self, obj):
        """Подписан ли пользователь на автора."""
        request = self.context.get('request')
        # if not request or not request.user.is_authenticated:
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, author=obj).exists()

    def create(self, validated_data):
        """Создание нового пользователя."""
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# class UserCreateSerializer(UserCreateSerializer):
#     """Регистрация нового пользователя.
#     с помощью djoser сериализатора UserCreateSerializer
#     """
#     class Meta:
#         model = CustomUser
#         fields = (
#             'email', 'id', 'username', 'first_name', 'last_name', 'password'
#         )
#         required_fields = (
#             'email', 'username', 'first_name', 'last_name', 'password'
#        )

# class SetPasswordSerializer(SetPasswordSerializer):
#     """Установка пароля.
#     с помощью djoser сериализатора SetPasswordSerializer
#     """
#     current_password = serializers.CharField(
#         required=True,
#         label='Текущий пароль')

#     def validate(self, data):
#         user = self.context.get('request').user
#         if data['new_password'] == data['current_password']:
#             raise serializers.ValidationError({
#                 "new_password": "Пароли не должны совпадать"})
#         check_current = check_password(data['current_password'], user.password)
#         if check_current is False:
#             raise serializers.ValidationError({
#                 "current_password": "Введен неверный пароль"})
#         return data


class SubscritionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки пользователя(user) на автора(author)"""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user = self.context.get('request').user
        return Subscription.objects.filter(
            author=obj.author, user=user).exists()

    def get_recipes(self, obj):
        """Получение списка рецептов автора."""
        from api.serializers import ShortRecipeSerializer
        limit = self.context.get('request').GET.get('recipes_limit')
        recipe_obj = obj.author.recipes.all()
        if limit:
            recipe_obj = recipe_obj[:int(limit)]
        serializer = ShortRecipeSerializer(recipe_obj, many=True)
        return serializer.data

