from django.db import IntegrityError

from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet

from recipes.models import Ingredient, Recipe, Tag
from .filters import IngredientFilter, RecipesFilter
from .pagination import ApiPagination
from .permissions import IsAdmin
from .serializers import AdminUserSerializer, IngredientSerializer, TagSerializer, UserSerializer, SignupSerializer, CastomeUserSerializer
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


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = CastomeUserSerializer
    permission_classes = [permissions.AllowAny]
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
