from django.contrib import admin

from .models import (Recipe, Ingredient, Tag, IngredientRecipe,
                     Favorite, ShoppingCart)

EMPTY_VALUE = '-пусто-'


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    fields = ('ingredient', 'amount')
    # fields = ('ingredient', 'amount', 'measurement_unit')
    #
    # def render_measurement_unit(self, obj):
    #     measurement_unit = Ingredient.objects.get(measurement_unit=obj)
    #     return measurement_unit


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # list_display = ('name', 'author', 'favorites_count')
    list_display = ('id', 'name', 'author',)
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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE


admin.site.register(ShoppingCart)
