from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe

from .models import Subscription

User = get_user_model()

class CommonSubscribed(metaclass=serializers.SerializerMetaclass):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(author=author,
                                               user=user).exists()
        return False

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')

class CustomUserSerializer(UserSerializer, CommonSubscribed):
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        # extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def get_is_subscribed(self, author):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return Subscription.objects.filter(author=author,
    #                                            user=user).exists()
    #     return False


class MinifiedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer, CommonSubscribed):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',  'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    # def get_is_subscribed(self, author):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return Subscription.objects.filter(
    #             author=author,
    #             user=user
    #         ).exists()
    #     return False

    def get_recipes(self, author):
        recipes_limit = int(self.context['request'].GET.get('recipes_limit', 5))
        recipes = Recipe.objects.filter(author=author)[:recipes_limit]

        return MinifiedRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, author):
        return author.recipes.count()
