from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username, validate_first_last_name


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

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

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


class Follow(models.Model):
    """Модель подписки пользователя(user) на автора(author)."""
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
        ]

    def __str__(self):
        return self.author
