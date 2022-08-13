from rest_framework import serializers

from .models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        # В прошлом уроке fields = '__all__' изменили на:
        fields = ('name', 'color', 'birth_year')