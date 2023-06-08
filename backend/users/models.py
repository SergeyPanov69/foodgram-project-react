from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username, validate_first_last_name


class CustomUser(AbstractUser):
    """Модель Пользователя приложения 'Foodgram'."""
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя (Логин)',
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        validators=[validate_first_last_name],
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        validators=[validate_first_last_name],
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=64,
        blank=False,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]


    def __str__(self) -> str:
        return self.email


class Follow(models.Model):
    """Модель подписки пользователя(user) на автора(author)."""
    author = models.ForeignKey(
        to=CustomUser,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name = 'following',
    )
    user = models.ForeignKey(
        to=CustomUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name = 'follower',
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_folower'
            )
        ]

    def __str__(self) -> str:
        return f'Пользователь {self.user} подписан на {self.author}'