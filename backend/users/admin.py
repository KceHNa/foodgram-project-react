from django.contrib import admin

from .models import Follow, User

EMPTY_VALUE = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Модель User в интерфейсе администратора."""
    list_display = ('id', 'username', 'email', 'password')
    list_filter = ('email', 'username', )
    empty_value_display = EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Модель Follow в интерфейсе администратора."""
    list_display = ('id', 'user', 'author')
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE
