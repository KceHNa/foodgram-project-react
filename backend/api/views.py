from rest_framework import viewsets

from api.serializers import RecipeListSerializer, IngredientSerializer
from recipes.models import Recipe, Ingredient


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ингридиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
