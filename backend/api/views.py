from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientSearchFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CustomUserSerializer, FollowSerializer,
    IngredientSerializer, MinimumRecipeSerializer,
    RecipeListSerializer, RecipeSerializer,
    TagSerializer, FollowValidateSerializer
)
from api.utils import create_pdf
from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe,
    ShoppingCart, Tag
)
from users.models import Follow, User


class CustomUserViewSet(UserViewSet):
    """
    Пользователи и подписки.
    Выводит подписки на авторов с рецептами.
    Создать подписку (подписаться), удалить подписку (отписаться).
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        """Мои подписки списком."""
        queryset = User.objects.filter(following__user=self.request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
    )
    def subscribe(self, request, id=None):
        """Подписка/отписка от автора."""
        user = request.user
        author = get_object_or_404(User, pk=id)
        data = {
            'user': user.id,
            'author': id
        }
        serializer = FollowValidateSerializer(
            data=data,
            context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Follow, user=user, author=author
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Подписка на данного пользователя невозможна'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Рецепты.
    Избранные рецепты (добавить/удалить),
    рецепыт с игридиентами в корзине (добавить/удалить)
    """
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def __post_method(model, pk, user):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен в список'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        return Response(
            MinimumRecipeSerializer(recipe).data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def __delete_method(model, pk, user):
        obj = get_object_or_404(model, user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Данного рецепта нет в списке'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        return self.__post_method(Favorite, pk=pk, user=request.user)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.__delete_method(Favorite, pk=pk, user=request.user)

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk):
        return self.__post_method(ShoppingCart, pk=pk, user=request.user)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.__delete_method(ShoppingCart, pk=pk, user=request.user)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Скачать список покупок."""
        shopping_cart = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values_list(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(count=Sum('amount'))
        shopping_file = create_pdf(shopping_cart)
        return shopping_file


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    """Список тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
