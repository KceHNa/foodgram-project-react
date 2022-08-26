from django.contrib import admin

from .models import Recipe, Ingredient, Tag, IngredientRecipe

EMPTY_VALUE = '-пусто-'


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    # list_display = ('name',)
    # measurement_unit = Ingredient.objects.filter()
    fields = ('ingredient','amount',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # list_display = ('name', 'author', 'favorites_count')
    list_display = ('name', 'author',)
    inlines = (IngredientRecipeInline,)
    empty_value_display = EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE
