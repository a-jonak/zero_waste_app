from django.contrib import admin

from .models import ProductInstance, Recipe


class RecipeAdmin(admin.ModelAdmin):
    pass


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'expiration_date', 'number', 'user')
    list_filter = ('expiration_date', 'user')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ProductInstance, ProductsAdmin)