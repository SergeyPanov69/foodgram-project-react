from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import AuthorOrReadOnly
from users.models import CustomUser
from users.serializers import (CustomUserSerializer, SetPasswordSerializer,
                               UserCreateSerializer)
# from api_yamdb.settings import ADMIN_EMAIL

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Cписок всех пользователей. Права доступа: Администратор"""
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return UserCreateSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # @action(
    #     detail=False,
    #     # methods=['GET', 'PATCH'],
    #     # url_path='me',
    #     permission_classes=(IsAuthenticated,)
    # )
    # def subscriptions(self, request):
    #     queryset = Subscribe.objects.filter(user=request.user)
    #     pages = self.paginate_queryset(queryset)
    #     serializer = SubscribeSerializer(
    #         pages,
    #         many=True,
    #         context={'request': request},)
    #     return self.get_paginated_response(serializer.data)
