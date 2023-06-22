# Generated by Django 3.2.3 on 2023-06-21 07:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_remove_favorite_recipe_has_been_already_added_in_favorites'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='amount',
            name='\nrecipes_amount ингридиент уже добавлен\n',
        ),
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe_author',
        ),
        migrations.AlterField(
            model_name='amount',
            name='amount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, 'Нужно добавить количество, минимум 1'), django.core.validators.MaxValueValidator(10000, 'Не много? Проверьте.')], verbose_name='Количество'),
        ),
        migrations.AddConstraint(
            model_name='amount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='ingredient_has_been_already_added_in_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='recipe_has_been_already_added_in_favorites'),
        ),
    ]
