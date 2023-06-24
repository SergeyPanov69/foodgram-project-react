from django.contrib import admin
from django.contrib.auth.models import Group

from recipes.models import Favorite, Amount, ShoppingCart
from users.models import Follow, User


class AmountInLine(admin.StackedInline):
    model = Amount


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
