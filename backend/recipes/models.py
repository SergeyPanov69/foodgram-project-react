from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингридиент: название, ед.измерения"""
    name = models.CharField(verbose_name="Ингредиент", max_length=200)
    measure_unit = models.CharField(max_length=50, verbose_name='Ед.изм.')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('name', 'measure_unit')
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name')

    def __str__(self):
        return f'{self.name}, {self.measure_unit}'


class Tag(models.Model):
    """Модель Слаг.
    Название, Цветовой HEX-код (например, #49B64E), Slug.
    """
    name = models.CharField(verbose_name='Тег', max_length=200, unique=True)
    color = models.CharField(verbose_name='Цвет', max_length=7, unique=True)
    slug = models.SlugField(verbose_name='Tag Slug', max_length=128, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ('name')

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
        to=User,
        on_delete=models.SET_NULL,
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
        through='IngredientAmount',
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/images',
    )

    cook_time = models.PositiveSmallIntegerField(
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
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'author', ),
                name='unique_recipe_author',
            ),
        ]

    def __str__(self) -> str:
        return f'Автор: {self.author.username} Рецепт: {self.name}'


class IngredienQuantity(models.Model):
    """Количество ингредиентов.
    Наполнение Рецепта(Recipe) количеством ингредиентов(Ingredient)."""
    recipe = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        related_name='В блюде',
    )
    ingredients = models.ForeignKey(
        verbose_name='Ингредиент в блюде',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
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
                fields=('recipe', 'ingredients', ),
                name='\n%(app_label)s_%(class)s ингридиент уже добавлен\n',
            ),
        ]

    def __str__(self):
        return f'{self.quantity} {self.ingredients}'

class LikeRecipe(models.Model):
    """Избранные пользователем(user) рецепты(recipe)."""
    user = models.ForeignKey(
        verbose_name='Пользователь',
        related_name='user_who_like',
        to=User, # Кто лайкает рецепт себе
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
        related_name='add_date',
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
    """Рецепты в корзину.
     Для подсчета суммарного количества ингридентов в закупке."""
    user = models.ForeignKey(
        verbose_name='Покупатель',
        related_name='buyer',
        to=User, # Кто покупает продукты
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
        related_name='add_date',
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

