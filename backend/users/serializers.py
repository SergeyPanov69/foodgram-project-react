from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from djoser.serializers import (SetPasswordSerializer,
                                UserSerializer, UserCreateSerializer)
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator


from users.validators import validate_username
from users.models import Follow, CustomUser

User = get_user_model()

class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()

    # def create(self, validated_data):
    #     """Регистрация нового пользователя."""
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        required_fields = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )

class SetPasswordSerializer(SetPasswordSerializer):
    current_password = serializers.CharField(
        required=True,
        label='Текущий пароль')

    def validate(self, data):
        user = self.context.get('request').user
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError({
                "new_password": "Пароли не должны совпадать"})
        check_current = check_password(data['current_password'], user.password)
        if check_current is False:
            raise serializers.ValidationError({
                "current_password": "Введен неверный пароль"})
        return data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author']
            )
        ]

        def validate(self, data):
            if data['user'] == data['following']:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя'
                )
            return data

