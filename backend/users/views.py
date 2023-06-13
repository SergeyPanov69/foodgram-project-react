from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
# from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# from rest_framework.routers import APIRootView

# from api.permissions import AuthorOrReadOnly
from users.models import CustomUser, Subscription
from users.serializers import (CustomUserSerializer, SubscritionSerializer,
                               SetPasswordSerializer, UserCreateSerializer)
# from api_yamdb.settings import ADMIN_EMAIL

# User = get_user_model()


# class APIRootView(APIRootView):
    # ...


class CustomUserViewSet(UserViewSet):
    """Работа с пользователями.
    Основан на UserViewSet пакета djoser.
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class=CustomUserSerializer

    @action(detail=False, methods=['get'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(
        detail=False,
        # methods=['GET', ],
        url_path='subscriptions',
        url_name='subscriptions', # Нужен?
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        """Список авторов, на которых подписан пользователь"""
        user = request.user
        queryset = Subscription.objects.filter(user=request.user) # Проверить правильно ли?
        pages = self.paginate_queryset(queryset)
        serializer = SubscritionSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='subscribe',
        url_name='subscribe', # Нужно?
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        """Подписаться на автора."""
        user = request.user
        author = get_object_or_404(CustomUser, id=id)

        if user == author:
            return Response(
                {'errors': 'На себя нельзя подписаться / отписаться'},
                status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.filter(
            author=author, user=user)
        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    {'errors': 'Нельзя подписаться повторно'},
                    status=status.HTTP_400_BAD_REQUEST)
            queryset = Subscription.objects.create(author=author, user=user)
            serializer = SubscritionSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {'errors': 'Вы уже отписаны'},
                    status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
