from django.contrib import admin

from .models import Product, UserProduct, Recipe, RecipeIngredient, UserShoppingList


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class UserProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'expiration_date', 'number', 'user')
    list_filter = ('expiration_date', 'user')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount', 'unit')
    list_filter = ('recipe', 'ingredient')


class UserShoppingListAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserProduct, UserProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(UserShoppingList, UserShoppingListAdmin)
