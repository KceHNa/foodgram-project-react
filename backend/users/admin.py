from django.contrib import admin

from .models import User

EMPTY_VALUE = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Модель User в интерфейсе администратора."""
    list_display = ('id', 'username', 'email', 'password')
    list_filter = ('email', 'username', )
    empty_value_display = EMPTY_VALUE
