from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('users.urls')),
    path('', include('recipes.urls')),
]
