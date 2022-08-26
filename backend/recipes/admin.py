from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Recipe, Ingredient, Tag, IngredientRecipe

EMPTY_VALUE = '-пусто-'


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    ields = ('ingredient', 'amount')
    # measurement_unit = Ingredient.objects.filter()
    # fields = ('ingredient', 'amount', 'measurement_unit')
    #
    # def measurement_unit(self, obj):
    #     return mark_safe("""%s""" % obj.measurement_unit)


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
