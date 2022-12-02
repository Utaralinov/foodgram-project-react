from djoser.serializers import UserSerializer

from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag

from users.models import User, username_validator


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipesCreatSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    # ingrediends = 

    class Meta:
        model = Recipe
        fields = '__all__'


class UsernameValidationMixin:

    def validate_username(self, value):
        return username_validator(value)


class CastomeUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first name'], 
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    # class Meta:
    #     model = User
    #     fields = ('email', 'username', 'first_name', 'last_name', 'password')



# class AdminUserSerializer(UsernameValidationMixin,
#                           serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'username', 'email', 'first_name', 'last_name', 'bio', 'role',
#         )


# class UserSerializer(AdminUserSerializer):

#     class Meta(AdminUserSerializer.Meta):
#         read_only_fields = ('role',)



class AdminUserSerializer(UsernameValidationMixin,
                          serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserSerializer(AdminUserSerializer):

    class Meta(AdminUserSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(UsernameValidationMixin, serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )
