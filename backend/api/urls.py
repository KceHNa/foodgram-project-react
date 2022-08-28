from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (RecipesViewSet, IngredientsViewSet,
                       CustomUserViewSet, TagsViewSet, FollowViewSet,
                       FollowListViewSet,)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'tags', TagsViewSet, basename='tags')


urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListViewSet.as_view(),
        name='subscriptions'),
    path(
        'users/<int:pk>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
