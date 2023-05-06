from django.urls import include, path

app_name = 'api'


urlpatterns = [
    path('', include('api.manager.urls')),
    path('', include('api.users.urls')),
    path('', include('api.ingridients.urls')),
    path('', include('api.recipes.urls')),
    path('', include('api.tags.urls')),
]
