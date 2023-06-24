from django.contrib import admin

from recipes.models import Amount, Ingredient, Recipe, Tag


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
