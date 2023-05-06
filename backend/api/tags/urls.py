from django.urls import include, path
from rest_framework import routers

from api.tags.views import TagViewSet

router = routers.DefaultRouter()


router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]