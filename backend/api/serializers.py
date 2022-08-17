from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, IngredientRecipe

from users.models import User


class CustomUserSerializer(UserSerializer):
    # is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeListSerializer(
        many=True,
        source='ingredient_recipe'
    )

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
