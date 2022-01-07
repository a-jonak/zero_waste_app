from django.contrib import admin

from .models import Product, ProductInstance, Recipe, RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'expiration_date', 'number', 'user')
    list_filter = ('expiration_date', 'user')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount', 'unit')
    list_filter = ('recipe', 'ingredient')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ProductInstance, ProductInstanceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)