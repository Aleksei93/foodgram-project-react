from django.urls import include, path
from rest_framework import routers

from api.views import (FavoriteManageView, IngredientViewSet,
                       ListFollowViewSet, RecipeViewSet,
                       ShoppingCartManageView, SubscriptionsManageView,
                       TagViewSet, download_shopping_cart)

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

subscriptions_urlpatterns = [
    path('subscriptions/', ListFollowViewSet.as_view(), name='subscriptions'),
    path(
        '<int:pk>/subscribe/', SubscriptionsManageView.as_view(),
        name='subscribe'),
]
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
    path('users/', include(subscriptions_urlpatterns)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]