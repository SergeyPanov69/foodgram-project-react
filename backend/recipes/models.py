# from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import CustomUser
from users.validators import color_validator

# User = get_user_model()


class Ingredient(models.Model):
    """Модель ингридиент: название, ед.измерения"""
    name = models.CharField(
        verbose_name="Ингредиент",
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Ед.изм.',
        max_length=50,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit', ),
                name='unique_ingredient'
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель Слаг.
    Название, Цветовой HEX-код (например, #49B64E), Slug.
    """
    name = models.CharField(
        verbose_name='Тег',
        max_length=200,
        unique=True,
        )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=[color_validator],
        )
    slug = models.SlugField(
        verbose_name='Tag Slug',
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ('name', )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель Рецептов блюд."""
    name = models.CharField(
        verbose_name = 'Название блюда',
        max_length=200,
    )
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='recipes',
        to=CustomUser,
        on_delete=models.CASCADE,
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание, Как готовить'
    )
    tags = models.ManyToManyField(
        verbose_name='Тег',
        related_name='recipes',
        to=Tag,
    )
    ingredients = models.ManyToManyField(
        verbose_name='Ингредиенты',
        related_name='recipes',
        to=Ingredient,
        through='recipes.IngredientQuantity',
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/images',
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=1,
        validators=(MinValueValidator(1, 'Минимальное время 1 мин.'),),

    )
    publish_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-publish_date', )
        constraints = [
            UniqueConstraint(
                fields=('name', 'author', ),
                name='unique_recipe_author',
            ),
        ]

    def __str__(self) -> str:
        return f'Автор: {self.author.username} Рецепт: {self.name}'


class IngredientQuantity(models.Model):
    """Количество ингредиентов.
    Наполнение Рецепта(Recipe) количеством ингредиентов(Ingredient)."""
    recipe = models.ForeignKey(
        verbose_name='В блюде',
        related_name='ingredient',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        verbose_name='Ингредиент в блюде',
        related_name='recipe',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Кол-во",
        default=0,
        validators=(
            MinValueValidator(1, 'Нужно добавить количество',),
            MaxValueValidator(1000, 'Не много? Проверьте.',),
        ),
    )

    class Meta:
        verbose_name = 'Кол-во ингридиента'
        verbose_name_plural = 'Кол-во ингридиентов'
        ordering = ('recipe', )
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'ingredient', ),
                name='\n%(app_label)s_%(class)s ингридиент уже добавлен\n',
            ),
        ]

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favorite(models.Model):
    """Любимые рецепты(recipe) пользователя(user)."""
    user = models.ForeignKey(
        verbose_name='Пользователь',
        related_name='user_who_like',
        to=CustomUser, # Кто лайкает рецепт себе
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name='Любимый рецепт',
        related_name='liked_recipe',
        to=Recipe, # Рецепт, который лайкают себе
        on_delete=models.CASCADE,
    )
    add_date=models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe', ),
                name='\n%(app_label)s_%(class)s рецепт уже в избранных\n',
            ),
        ]

    def __str__(self):
        return (f'Пользователь:{self.user.username}'
                f'Любимый рецепт:{self.recipe.name}'
            )


class Shopping(models.Model):
    """Рецепты в корзине.
     Для подсчета суммарного количества ингридентов в закупке."""
    user = models.ForeignKey(
        verbose_name='Покупатель',
        related_name='buyer',
        to=CustomUser, # Кто покупает продукты
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name='Рецепты для списка покупок',
        related_name='purchase_recipe',
        to=Recipe, # Рецепт, для которого покупают продукты
        on_delete=models.CASCADE,
    )
    add_date=models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт для закупки'
        verbose_name_plural = 'Рецепты для закупки'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe', ),
                name='\n%(app_label)s_%(class)s рецепт уже в корзине\n',
            ),
        ]
    def __str__(self):
        return f'Пользователь: {self.user} Cписок рецептов: {self.recipe}'

