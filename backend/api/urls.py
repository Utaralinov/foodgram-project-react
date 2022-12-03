from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipesViewSet, TagViewSet, UserViewSet, SubscriptionViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<int:id>/subscribe/', SubscriptionViewSet.as_view({'post': 'create'}), name='subscribe'),
    path('', include(router.urls)),
    # path('api/users/', signup, name='signup'),
]
