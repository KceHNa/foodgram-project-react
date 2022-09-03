from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomUserViewSet, FollowViewSet, IngredientsViewSet,
    RecipesViewSet, TagsViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')


urlpatterns = [
    path(
        'users/<int:pk>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
