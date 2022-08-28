from os import path

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import RecipeFilter, IngredientSearchFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (RecipeListSerializer, IngredientSerializer,
                             CustomUserSerializer, TagSerializer,
                             FollowSerializer, MinimumRecipeSerializer, )
from foodgramm.settings import BASE_DIR
from recipes.models import (Recipe, Ingredient, Tag, Favorite,
                            IngredientRecipe, ShoppingCart)
from users.models import User, Follow

DOCUMENT_TITLE = 'Foodgramm, «Продуктовый помощник»'
FONT_NAME = 'shoppingcart'
FONT_PATH = path.join(BASE_DIR, f'../data/{FONT_NAME}.ttf')
SHOPPING_CART_TEMPLATE = '• {} ({}) - {}'


class CustomUserViewSet(UserViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Рецепты.
    Избранные рецепты (добавить/удалить),
    рецепыт с игридиентами в корзине (добавить/удалить)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    # def get_serializer_class(self):
    #     if self.request.method in ('POST', 'PATCH'):
    #         return RecipeListSerializer
    #     return MinimumRecipeSerializer

    @staticmethod
    def post_method(model, user, pk):
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
    def delete_method(request, pk, model):
        obj = model.objects.filter(user=request.user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Данного рецепта нет в списке'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        return self.post_method(Favorite, pk=pk, user=request.user)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk):
        return self.post_method(ShoppingCart, pk=pk, user=request.user)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method(
            request=request, pk=pk, model=ShoppingCart)

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
        pdfmetrics.registerFont(
            TTFont(FONT_NAME, FONT_PATH, 'UTF-8')
            )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment;''filename="shopping_cart.pdf"'
            )
        pdf_doc = canvas.Canvas(response)
        pdf_doc.setTitle(DOCUMENT_TITLE)
        pdf_doc.setFont(FONT_NAME, size=32)
        pdf_doc.drawCentredString(300, 800, 'Список покупок')
        pdf_doc.line(100, 780, 480, 780)
        pdf_doc.setFont(FONT_NAME, size=16)
        height = 750
        for ingredient in shopping_cart:
            pdf_doc.drawString(
                75, height, (SHOPPING_CART_TEMPLATE.format(*ingredient))
            )
            height -= 25
        pdf_doc.showPage()
        pdf_doc.save()
        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ингридиенты."""
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


class FollowViewSet(APIView):
    """
    Создать подписку (подписаться), удалить подписку (отписаться).
    """
    permission_classes = (IsAuthenticated,)

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
    """Список подписок."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
