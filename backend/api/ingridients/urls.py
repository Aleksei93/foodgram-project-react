from django.urls import include, path
from rest_framework import routers

from api.ingridients.views import IngredientViewSet

router = routers.DefaultRouter()


router.register('ingredients', IngredientViewSet, basename='ingredientsss')

urlpatterns = [
    path('', include(router.urls)),
]
