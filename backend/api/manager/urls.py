from django.urls import include, path
from api.manager.views import SubscriptionsManageView, ListFollowViewSet

subscriptions_urlpatterns = [
    path('subscriptions/', ListFollowViewSet.as_view(), name='subscriptions'),
    path(
        '<int:pk>/subscribe/', SubscriptionsManageView.as_view(),
        name='subscribe'),
]

urlpatterns = [
    path('users/', include(subscriptions_urlpatterns)),
]
