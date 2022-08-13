from django.db import models


class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=150)

    def __str__(self):
        return self.name
    