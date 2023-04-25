from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import RecipeFilter
from api.pagination import CustomPageNumberPagination
from api.permissions import RecipePermissions
from api.serializers import (RecipeCreateUpdateSerializer,
                             RecipeSerializerList)
from recipes.models import Recipe

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (RecipePermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializerList

        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
