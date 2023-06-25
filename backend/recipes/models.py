from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.validators import color_validator, validate_username

User = get_user_model()


class Tag(models.Model):
    """Модель Слаг.
    Название, Цветовой HEX-код (например, #49B64E), Slug.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=[color_validator],
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиент: название, ед.измерения"""
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=32
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

    def clean(self) -> None:
        self.name = self.name.lower()
        self.measurement_unit = self.measurement_unit.lower()
        super().clean()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецептов блюд."""
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        validators=[validate_username]
    )
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='recipes',
        to=User,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Описание, Как готовить'
    )
    tags = models.ManyToManyField(
        verbose_name='Теги',
        related_name='recipes',
        to=Tag,
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='images/',
        null=True,
        default=None
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=1,
        validators=(
            MinValueValidator(1, 'Минимальное время 1 мин.'),
            MaxValueValidator(
                1440, 'Не многовато ли? Максимально 1440 мин. - это 24 часа.'
            )
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    amount_ingredients = models.ManyToManyField(
        Ingredient, through='Amount'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
        constraints = [
            UniqueConstraint(
                fields=('name', 'author', ),
                name='unique_recipe_author',
            ),
        ]

    def __str__(self):
        return self.name


class Amount(models.Model):
    """Количество ингредиентов.
    Наполнение Рецепта(Recipe) количеством ингредиентов(Ingredient)."""
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=(
            MinValueValidator(1, 'Нужно добавить количество, минимум 1',),
            MaxValueValidator(10000, 'Не много? Проверьте.',),
        ),
    )
    ingredient = models.ForeignKey(
        related_name='amounts',
        verbose_name='Ингредиент',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        related_name='ingredients',
        verbose_name='Рецепт',
        to=Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredient_has_been_already_added_in_recipe',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount} в {self.recipe}'


class ShoppingCart(models.Model):
    """Рецепты в корзине.
     Для подсчета суммарного количества ингридентов в закупке."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name='В корзине',
        related_name='in_shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe_has_been_already_added_in_shoppingcart',
            ),
        ]

    def __str__(self):
        return f'{self.user} добавил в корзину {self.recipe}'


class Favorite(models.Model):
    """Любимые рецепты(recipe) пользователя(user)."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name='В избранном',
        related_name='favorited'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe_has_been_already_added_in_favorites',
            ),
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'
