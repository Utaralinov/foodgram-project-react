from django.db import IntegrityError
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Ingredient, Recipe, Tag, Subscription
from .filters import IngredientFilter, RecipesFilter
from .pagination import ApiPagination
from .permissions import IsAdmin
from .serializers import (IngredientSerializer, TagSerializer,
                          CustomUserSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          SubscriptionSerializer)
from users.models import User

USER_CREATION_ERROR = ('Ошибка создания пользователя - '
                       'нарушена уникальность имейла и юзернейма')


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientFilter)
    search_fields = ['^name']
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = RecipesFilter
    pagination_class = ApiPagination
    serializer_class = RecipeCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(serializer.validated_data['current_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"current_password": ["Неверный пароль."]}, status=status.HTTP_400_BAD_REQUEST)


#     permission_classes = (IsAdmin,)
#     filter_backends = (filters.SearchFilter,)
#     lookup_field = 'username'
#     search_fields = ('username',)

#     @action(
#         detail=False,
#         methods=['get', 'patch'],
#         url_path='me',
#         url_name='me',
#         permission_classes=(IsAuthenticated,)
#     )
#     def about_me(self, request):
#         serializer = UserSerializer(request.user)
#         if request.method != 'PATCH':
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         serializer = UserSerializer(
#             request.user, data=request.data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     subject = 'Код подтверждения'
#     try:
#         user, created = User.objects.get_or_create(
#             username=serializer.validated_data["username"],
#             email=serializer.validated_data["email"],
#         )
#     except IntegrityError:
#         return Response(USER_CREATION_ERROR,
#                         status=status.HTTP_400_BAD_REQUEST)
#     return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return get_list_or_404(User, author__user=self.request.user)

    def create(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        author = get_object_or_404(User, pk=pk)
        user = request.user
    
        if user == author:
            return Response({'errors': 'Нельзя подписатся на самого себя.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        elif Subscription.objects.filter(author=author, user=user).exists():
            return Response({'errors': 'Вы уже подписаны.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        subscription = Subscription(author=author, user=user)
        subscription.save()

        serializer = SubscriptionSerializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)