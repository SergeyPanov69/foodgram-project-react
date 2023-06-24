from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

User = get_user_model()


class UsersSerializer(UserSerializer):
    """Сериалайзер пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователя на автора."""
        request = self.context.get('request')
        subcribe = request.user.follower.filter(author=obj)
        return (
            subcribe.exists()
            and request.user.is_authenticated
        )
