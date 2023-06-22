from django.contrib import admin
from django.contrib.auth.models import Group

from recipes.models import (Favorite, Amount, Ingredient,
                            Recipe, ShoppingCart, Tag)
from users.models import Follow, User


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    empty_value_display = "-пусто-"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_editable = ('name', 'measurement_unit', )
    search_fields = ('name', )
    list_filter = ('name', )


class AmountInLine(admin.StackedInline):
    model = Amount


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'image',
        'count_in_favorites'
    )
    list_filter = ('name', 'author', 'tags', )
    search_fields = ('name', 'author', )
    inlines = [AmountInLine, ]
    readonly_fields = ('count_in_favorites', )

    def count_in_favorites(self, obj):
        return obj.favorited.count()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name',
    )
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'
    list_filter = ('last_name', 'email',)


@admin.register(Follow)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


admin.site.unregister(Group)
