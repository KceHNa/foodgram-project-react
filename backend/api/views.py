from rest_framework import viewsets

from recipes.models import Recipe


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.all()
