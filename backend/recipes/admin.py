from django.contrib import admin

from .models import Recipe, Ingredient

EMPTY_VALUE = '-пусто-'


admin.site.register(Recipe)
admin.site.register(Ingredient)
