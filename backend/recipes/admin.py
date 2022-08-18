from django.contrib import admin
from django.utils.html import format_html

from .models import Recipe, Ingredient, Tag

EMPTY_VALUE = '-пусто-'


admin.site.register(Recipe)
admin.site.register(Ingredient)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE
