from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# from fpdf import FPDF
from rest_framework import filters, status, viewsets
from rest_framework import response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, SAFE_METHODS)
from rest_framework.decorators import action

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             ShortRecipeSerializer, SubscribeSerializer,
                             TagSerializer)
from recipes.models import (Ingredient, IngredientQuantity, Favorite,
                            Recipe, Shopping, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьесет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None,
    # filter_backends = (filters.SearchFilter,) # Надо проверять
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrReadOnly)
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add(self, model, user, pk, name):
        """Добавление рецепта в список пользователя."""
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if relation.exists():
            return response.Response(
                {'errors': f'Нельзя повторно добавить рецепт в {name}'},
                status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, model, user, pk, name):
        """"Удаление рецепта из списка пользователя."""
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return response.Response(
                {'errors': f'Нельзя повторно удалить рецепт из {name}'},
                status=status.HTTP_400_BAD_REQUEST)
        relation.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
            methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
            url_name='favorite'
    )
    def favorite(self, request, pk=None):
        """Добавление и удаление рецептов - Избранное."""
        user = request.user
        if request.method == 'POST':
            name = 'избранное'
            return self.add(Favorite, user, pk, name)
        if request.method == 'DELETE':
            name = 'избранного'
            return self.delete_relation(Favorite, user, pk, name)
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
            methods=['post', 'delete'],
            detail=True,
            url_path='shopping_cart',
            url_name='shopping_cart'
    )
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецептов - Список покупок."""
        user = request.user
        if request.method == 'POST':
            name = 'список покупок'
            return self.add(Shopping, user, pk, name)
        if request.method == 'DELETE':
            name = 'списка покупок'
            return self.delete_relation(Shopping, user, pk, name)
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
            methods=['get'],
            detail=False,
            url_path='download_shopping_cart',
            url_name='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        """Формирование и скачивание списка покупок."""
        user = request.user
        ingredients = (
            IngredientQuantity.objects
            .filter(recipe__purchase_recipe__user=user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(Sum('amount', distinct=True))
        )

        shopping_cart = '\n'.join([
            f'{i["ingredients__name"]} '
            f'({i["ingredients__measurement_unit"]}) – '
            f'{i["amount"]}'
            for i in ingredients
        ])



        response = HttpResponse(shopping_cart,
            content_type='text/plain', status=status.HTTP_200_OK)
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"')

        return response