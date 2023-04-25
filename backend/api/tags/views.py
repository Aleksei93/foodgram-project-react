from django.contrib.auth import get_user_model

from api.mixins import ListRetrieveViewSet
from api.tags.serializers import TagSerializer
from recipes.models import Tag

User = get_user_model()


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
