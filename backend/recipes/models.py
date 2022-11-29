from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()

class Tag(models.Model):
    """ -- Теги -- """

    name = models.CharField(verbose_name='Название', max_length=200)
    color = models.CharField(
        verbose_name='Цвет в HEX',
        unique=True,
        max_length=7
    )
    slug = models.SlugField(verbose_name='Слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """ -- Ингредиенты -- """

    name = models.CharField(verbose_name='Ингредиент', max_length=200)
    measurement_unit = models.CharField(verbose_name='Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ -- Рецепт -- """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField(
        'Фото',
        upload_to='image_recipes/',
    )
    text = models.TextField('Описание', max_length=1000)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время в минутах',
        validators=[MinValueValidator(1, 'Время приготовления')]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """ -- Ингредиент в рецепте -- """

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент рецепта',
        on_delete=models.CASCADE,
        related_name='recipeIngredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipeIngredient'
    )
    amount = models.PositiveIntegerField(
        'Количество ингредиента',
        validators=[MinValueValidator(1, 'Количество ингредиента')]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'
