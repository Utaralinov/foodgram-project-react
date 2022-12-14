from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


class SubscriptionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return get_list_or_404(User, author__user=self.request.user)

    def create(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        author = get_object_or_404(User, pk=pk)
        user = request.user

        if user == author:
            return Response({'errors': 'Нельзя подписатся на самого себя.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(author=author, user=user).exists():
            return Response({'errors': 'Вы уже подписаны.'},
                            status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscription(author=author, user=user)
        subscription.save()

        serializer = self.get_serializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        author = get_object_or_404(User, pk=pk)
        user = request.user

        subscription = get_object_or_404(Subscription, user=user, author=author)
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
