from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'email', 'username', 'first_name', 'last_name',
    )
    search_fields = ('username', 'email',)
    empty_value_display = 'Пусто'
    list_filter = ('last_name', 'email',)
