from django.contrib.auth.models import AbstractUser
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import RecipesViewSet

app_name = 'api'

router_v1 = SimpleRouter('')
# router_v1.register(r'users', AbstractUser, basename='users')
router_v1.register(
    'recipes',
    RecipesViewSet,
    basename='recipes'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('', include('users.urls')),
]
