
from rest_framework import mixins, permissions, viewsets


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (permissions.AllowAny,)
