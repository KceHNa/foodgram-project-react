from djoser.views import UserViewSet
from rest_framework import viewsets

from api.serializers import (RecipeListSerializer, IngredientSerializer,
                             CustomUserSerializer,)
from recipes.models import Recipe, Ingredient
from users.models import User


class CustomUserViewSet(UserViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ингридиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
