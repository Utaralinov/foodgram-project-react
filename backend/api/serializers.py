from djoser.serializers import UserSerializer

from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag, RecipeIngredient, Subscription

from users.models import User, username_validator



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


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug')


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_subscribed']
        # read_only_fields = ('is_subscribed',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                author=author,
                user=user
            ).exists()
        return False


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(source=('recipeIngredient'),
                                             many=True,
                                             read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ("id",
                  "tags",
                  "author",
                  "ingredients",
                  "name",
                  "image",
                  "text",
                  "cooking_time")

    def validate_ingredients(self, value):
        validated_ingredients = []
        for ingredient in value:
            object = ingredient['id']
            if object.id in validated_ingredients:
                raise serializers.ValidationError('Данный ингредиент повторяется в рецепте.')
            validated_ingredients.append(object.id)
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user, **validated_data
        )
        recipe.tags.set(tags)
        for ingredient in ingredients:
            # raise serializers.ValidationError(ingredient)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        # recipe.save()
        return recipe


class PasswordSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField(
        max_length=150,
        required=True,
    )
    current_password = serializers.CharField(
        max_length=150,
        required=True,
    )


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',  'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                author=author,
                user=user
            ).exists()
        return False

    def get_recipes(self, author):
        recipes_limit = int(self.context['request'].GET.get('recipes_limit', 5))
        recipes = Recipe.objects.filter(author=author)[:recipes_limit]
        return SubscriptionRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, author):
        return author.recipes.count()
