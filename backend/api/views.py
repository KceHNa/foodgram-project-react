from djoser.views import UserViewSet
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (RecipeListSerializer, IngredientSerializer,
                             CustomUserSerializer, TagSerializer,
                             FollowSerializer, )
from recipes.models import Recipe, Ingredient, Tag
from users.models import User, Follow


class CustomUserViewSet(UserViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    # @action(detail=False, methods=['get'],)
    # def subscriptions(self, request):
    #     """Получить на кого пользователь подписан."""
    #     user = self.request.user
    #     if user.is_anonymous:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     return Follow.objects.filter(user__username=user)


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ингридиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagsViewSet(viewsets.ModelViewSet):
    """Список тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FollowViewSet(APIView):
    """
    Создать подписку (подписаться), удалить подписку (отписаться).
    """
    def post(self, request, pk):
        if pk == request.user.id:
            return Response(
                {'error': 'Пользователь не может подписаться сам на себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(user=request.user, author_id=pk).exists():
            return Response(
                {'error': 'Подписка уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, pk=pk)
        Follow.objects.create(user=request.user, author_id=pk)
        return Response(
            FollowSerializer(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        get_object_or_404(User, id=pk)
        subscription = Follow.objects.filter(user=request.user, author_id=pk)
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Подписка на данного пользователя невозможна'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowListViewSet(ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
