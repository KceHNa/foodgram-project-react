from django.conf import settings
from django.contrib import admin

from .models import Follow, User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Модель User в интерфейсе администратора."""
    list_display = ('id', 'username', 'email', 'password')
    list_filter = ('email', 'username', )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Модель Follow в интерфейсе администратора."""
    list_display = ('id', 'user', 'author')
    list_filter = ('user',)
    empty_value_display = settings.EMPTY_VALUE
