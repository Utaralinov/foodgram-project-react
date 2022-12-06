from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ['name']
    search_fields = ('name',)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'in_favorite')
    list_filter = ['name', 'author', 'tags']
    inlines = [RecipeIngredientsInline]

    def in_favorite(self, obj):
        return obj.favorites.all().count()


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
