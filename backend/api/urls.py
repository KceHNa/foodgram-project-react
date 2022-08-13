from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import RecipesViewSet

app_name = 'api'

ver_1 = SimpleRouter('v1')
ver_1.register(
    'recipes',
    RecipesViewSet,
    basename='recipes'
)

urlpatterns = [
    path('v1/', include(ver_1.urls)),
    # path('v1/', include('djoser.urls.jwt')),
]