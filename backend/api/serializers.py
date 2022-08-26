from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, IngredientRecipe, Tag

from users.models import User, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    """Серилизатор создания пользователя."""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True, }}


class CustomUserSerializer(UserSerializer):
    """Серилизатор юзера с его подписками."""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')


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
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('__all__',)


class FollowSerializer(CustomUserSerializer):
    """Вывод подписок пользователя."""
    # recipes = serializers.SerializerMethodField()
    # recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  # 'is_subscribed', 'recipes', 'recipes_count')
                  'is_subscribed',)

        # def get_is_subscribed(self, obj):
        #     user = self.context['request'].user
        #     if user.is_anonymous:
        #         return False
        #     return Follow.objects.filter(
        #         user=user, author=obj.author
        #     ).exists()

        # def get_recipes_count(self, obj):
        #     return obj.recipes.count()

        # def get_recipes(self, obj):
        #     # limit = self.context['request'].query_params.get('recipes_limit')
        #     # if limit is None:
        #     #     recipes = obj.recipes.all()
        #     # else:
        #     #     recipes = obj.recipes.all()[:int(limit)]
        #     recipes = obj.recipes.all()
        #     recipes_limit = (self.context.get('request')
        #                      .query_params.get('recipes_limit')
        #                      )
        #     if recipes_limit:
        #         recipes = recipes[:int(recipes_limit)]
        #     return MinimumRecipeSerializer(recipes, many=True).data


class MinimumRecipeSerializer(serializers.ModelSerializer):
    """Краткое отображение рецептов."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)
