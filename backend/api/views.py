from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (RecipeListSerializer, IngredientSerializer,
                             CustomUserSerializer)
from recipes.models import Recipe, Ingredient
from users.models import User


# @api_view(['GET'])
# def about_me(request):
#     serializer = CustomUserSerializer(request.user)
#     return Response(serializer.data, status=status.HTTP_200_OK)


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
