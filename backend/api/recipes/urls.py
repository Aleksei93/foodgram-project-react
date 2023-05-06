from django.urls import include, path
from rest_framework import routers

from api.recipes.views import RecipeViewSet
from api.manager.views import (download_shopping_cart, ShoppingCartManageView,
                               FavoriteManageView)

router = routers.DefaultRouter()


router.register('recipes', RecipeViewSet, basename='recipes')

recipe_additional_urlpatterns = [
    path(
        'download_shopping_cart/', download_shopping_cart,
        name='download_shopping_cart'),
    path(
        '<int:pk>/shopping_cart/', ShoppingCartManageView.as_view(),
        name='shopping_cart'),
    path('<int:pk>/favorite/', FavoriteManageView.as_view(), name='favorites'),
]


urlpatterns = [
    path('recipes/', include(recipe_additional_urlpatterns)),
    path('', include(router.urls)),
]