from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import(AllowAny, IsAuthenticatedOrReadOnly,
                                       IsAuthenticated)
from rest_framework.response import Response

from .models import (Favorite, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)
from .filters import IngredientFilter, RecipesFilter
from .permissions import IsAuthorOrAdmin
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          MinifiedRecipeSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer,)
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
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            return self.add_favorite(user, recipe)

        if request.method == "DELETE":
            return self.delete_favorite(user, recipe)

    def add_favorite(self, user, recipe):
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response({"error": "Этот рецепт уже есть в избранном."},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        favorite = Favorite.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(favorite)
        # , context={"request": request}
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_favorite(self, user, recipe):
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if not favorite.exists():
            return Response({"error": "Этого рецепта нет в избранном."},
                            status=status.HTTP_400_BAD_REQUEST)

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST", "DELETE"])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            return self.add_to_shopping_cart(user, recipe)

        if request.method == "DELETE":
            return self.delete_from_shopping_cart(user, recipe)

    def add_to_shopping_cart(self, user, recipe):
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response({"error": "Этот рецепт уже есть в списке покупок."},
                            status=status.HTTP_400_BAD_REQUEST)
        shopoing_cart = ShoppingCart.objects.create(user=user,
                                                   recipe=recipe)
        serializer = ShoppingCartSerializer(shopoing_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from_shopping_cart(self, user, recipe):
        shopoing_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if not shopoing_cart.exists():
            return Response({"error": "Этого рецепта нет в списке покупок."},
                            status=status.HTTP_400_BAD_REQUEST)

        shopoing_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        return download_file_response(ingredients_list)
