from django.contrib import admin

from users.models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name',
    )
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'
    list_filter = ('last_name', 'email',)


@admin.register(Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    empty_value_display = '-пусто-'
