from os import path

from django.db.models import Sum
from django.http import HttpResponse
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (RecipeListSerializer, IngredientSerializer,
                             CustomUserSerializer, TagSerializer,
                             FollowSerializer, MinimumRecipeSerializer, )
from foodgramm.settings import BASE_DIR
from recipes.models import Recipe, Ingredient, Tag, Favorite, IngredientRecipe, ShoppingCart
from users.models import User, Follow

DOCUMENT_TITLE = 'Foodgramm, «Продуктовый помощник»'
FONT_NAME = 'shoppingcart'
FONT_PATH = path.join(BASE_DIR, f'../data/{FONT_NAME}.ttf')
SHOPPING_CART_TEMPLATE = '• {} ({}) - {}'


class CustomUserViewSet(UserViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


    @action(detail=True, methods=['POST', 'DELETE'],)
    def favorite(self, request, pk):
        current_user = self.request.user
        if current_user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_favorite = Favorite.objects.filter(user=current_user, recipe=recipe)
        if request.method == 'POST':
            serializer = MinimumRecipeSerializer(recipe)
            if recipe_in_favorite.exists():
                data = {'errors': 'Этот рецепт уже есть в избранном.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=current_user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not recipe_in_favorite.exists():
                data = {'errors': 'Этого рецепта нет в избранном пользователя.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            recipe_in_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
    )
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_shopping_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        )
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if not in_shopping_cart:
                shopping_cart = ShoppingCart.objects.create(
                    user=user,
                    recipe=recipe
                )
                serializer = MinimumRecipeSerializer(shopping_cart.recipe)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
        elif request.method == 'DELETE':
            if not in_shopping_cart:
                data = {'errors': 'Такой рецепта нет в списке покупок.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
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
    """Список подписок."""
    serializer_class = FollowSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
