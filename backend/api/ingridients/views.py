from django.conf import settings
from django.contrib.auth import get_user_model

from api.filters import IngredientsSearchFilter
from api.mixins import ListRetrieveViewSet
from api.ingridients.serializers import IngredientSerializer

from recipes.models import Ingredient

User = get_user_model()


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientsSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None
