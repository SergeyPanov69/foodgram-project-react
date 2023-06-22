from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import FavoriteSerializer
from recipes.models import Recipe


def add_to(self, model, user, pk, name):
    """Добавление рецепта в список пользователя."""
    recipe = get_object_or_404(Recipe, pk=pk)
    relation = model.objects.filter(user=user, recipe=pk)
    if relation.exists():
        return Response(
            {'errors': f'Нельзя повторно добавить рецепт в {name}.'},
            status=status.HTTP_400_BAD_REQUEST)
    instance = model.objects.create(user=user, recipe=recipe)
    serializer = FavoriteSerializer(instance)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def delete_from(self, model, user, pk, name):
    """"Удаление рецепта из списка пользователя."""
    recipe = get_object_or_404(Recipe, pk=pk)
    relation = model.objects.filter(user=user, recipe=recipe)
    if not relation.exists():
        return Response(
            {'errors': f'Рецепт уже удален из {name}'},
            status=status.HTTP_400_BAD_REQUEST)
    relation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
