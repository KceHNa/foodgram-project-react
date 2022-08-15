from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import RecipesViewSet

app_name = 'api'

router_ver1 = SimpleRouter('')
router_ver1.register(
    'recipes',
    RecipesViewSet,
    basename='recipes'
)

urlpatterns = [
    path('v1/', include(router_ver1.urls)),
    # path('v1/', include('djoser.urls.jwt')),
]