from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (Ingredient, Favorite, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)


User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class MinifiedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(source='recipeingredients',
                                             many=True,
                                             read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',)

    def get_is_favorited(self, recipe):
        return self.get_object(Favorite, recipe)

    def get_is_in_shopping_cart(self, recipe):
        return self.get_object(ShoppingCart, recipe)

    def get_object(self, model, recipe):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return model.objects.filter(recipe=recipe, user=request.user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(source='recipeingredients',
                                             many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'image', 'name', 'text', 'cooking_time')

    def create_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_recipe = RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            )

    def validate_ingredients(self, value):
        validated_ingredients = []
        for ingredient in value:
            ingredient_id = ingredient['ingredient']['id']
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError('Данного ингредиента нет в базе!')
            if ingredient_id in validated_ingredients:
                raise serializers.ValidationError('Данный ингредиент повторяется в рецепте.')
            validated_ingredients.append(ingredient_id)
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredients')
        recipe = Recipe.objects.create(author=self.context.get('request').user,
                                       **validated_data)
        recipe.tags.set(tags)
        self.create_recipe_ingredients(ingredients, recipe)

        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)

        ingredients = validated_data.pop('recipeingredients')
        recipe.ingredients.clear()
        self.create_recipe_ingredients(ingredients, recipe)

        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        context={'request': self.context.get('request')}
        return RecipeSerializer(recipe, context=context).data

class CommonFavoriteCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if self.metaclass.model.objects.filter(user=user, recipe__id=recipe_id).exists():
            raise ValidationError('Рецепт уже добавлен в избранное!')
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return MinifiedRecipeSerializer(instance.recipe, context=context).data

class FavoriteSerializer(CommonFavoriteCartSerializer):
    class Meta(CommonFavoriteCartSerializer.Meta):
        model = Favorite

class ShoppingCartSerializer(CommonFavoriteCartSerializer):
    class Meta(CommonFavoriteCartSerializer.Meta):
        model = ShoppingCart
