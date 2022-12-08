from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipesFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .permissions import IsAuthorOrAdmin
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .utils import download_file_response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientFilter)
    search_fields = ['^name']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=["POST", "DELETE"])
    def favorite(self, request, pk=None):
        return self.user_recipe_action(request, pk, Favorite, FavoriteSerializer)

    @action(detail=True, methods=["POST", "DELETE"])
    def shopping_cart(self, request, pk=None):
        return self.user_recipe_action(request, pk, ShoppingCart, ShoppingCartSerializer)

    def user_recipe_action(self, request, pk, model_class, serializer_class):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            return self.add_user_recipe_model(user, recipe, model_class, serializer_class)

        if request.method == "DELETE":
            return self.delete_user_recipe_model(user, recipe, model_class)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def add_user_recipe_model(self, user, recipe, model_class, serializer_class):
        if model_class.objects.filter(user=user, recipe=recipe).exists():
            return Response({"error": f"Этот рецепт уже есть в {model_class._meta.verbose_name.title()}."},
                            status=status.HTTP_400_BAD_REQUEST)
        model = model_class.objects.create(user=user, recipe=recipe)
        serializer = serializer_class(model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_user_recipe_model(self, user, recipe, model_class):
        model = model_class.objects.filter(user=user, recipe=recipe)
        if not model.exists():
            return Response({"error": f"Этого рецепта нет в {model_class._meta.verbose_name.title()}."},
                            status=status.HTTP_400_BAD_REQUEST)

        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(total=Sum('amount'))

        return download_file_response(ingredients_list)
