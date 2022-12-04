from django_filters import AllValuesMultipleFilter, BooleanFilter, FilterSet
from rest_framework import filters

from .models import Recipe


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug',
                                   lookup_expr="iexact",)
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            queryset = queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            queryset = queryset.filter(shopping_cart__user=self.request.user)
        return queryset
