from django.contrib.auth.models import AbstractUser
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import RecipesViewSet, IngredientsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
# router_v1.register(r'users', AbstractUser, basename='users')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('', include('users.urls')),
]
