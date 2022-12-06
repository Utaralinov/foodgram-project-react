from django.urls import include, path

from .views import SubscriptionViewSet

urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<int:id>/subscribe/',
         SubscriptionViewSet.as_view({'post': 'create',
                                      'delete': 'destroy'}),
         name='subscribe'),
    path('', include('djoser.urls')),
]
