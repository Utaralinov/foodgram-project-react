from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Ingredient
from .filters import IngredientFilter
from .serializers import IngredientSerializer



class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientFilter)
    search_fields = ['^name']
    permission_classes = [permissions.AllowAny]


