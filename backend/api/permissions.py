from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser


class AuthorOrReadOnly(permissions.BasePermission):
    """Автору доступ"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
            and request.user == obj.author
            )
            or request.user.is_superuser
        )

