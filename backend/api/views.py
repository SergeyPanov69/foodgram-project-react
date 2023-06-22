from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer,
                             RecipeSerializer,
                             RecipeWriteSerializer,
                             TagSerializer)
from api.permissions import AuthorOrReadOnly
from api.utils import add_to, delete_from
from recipes.models import (Amount, Favorite, Ingredient,
                            Recipe, ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
            url_name='favorite',
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        """Добавление и удаление рецептов в Избранное."""
        user = request.user
        if request.method == 'POST':
            name = 'избранное'
            return add_to(self, Favorite, user, pk, name)
        if request.method == 'DELETE':
            name = 'избранного'
            return delete_from(self, Favorite, user, pk, name)
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='shopping_cart',
            url_name='shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавление и удаление рецептов в список покупок"""
        user = request.user
        if request.method == 'POST':
            name = 'список покупок'
            return add_to(self, ShoppingCart, user, pk, name)
        if request.method == 'DELETE':
            name = 'списка покупок'
            return delete_from(self, ShoppingCart, user, pk, name)
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'],
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request, **kwargs):
        """Формирование и скачивание списка покупок."""
        user = request.user
        ingredients = (
            Amount.objects
            .filter(recipe__in_shopping_cart__user=user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name',
                         'ingredient__measurement_unit',
                         'total_amount'
                         )
        )

        shopping_cart = []
        [shopping_cart.append(
            '{} ({}) — {}'.format(*ingredient)) for ingredient in ingredients]
        response = HttpResponse(
            'Cписок покупок:\n' + '\n'.join(shopping_cart),
            content_type='text/plain',
            status=status.HTTP_200_OK
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"')
        return response
