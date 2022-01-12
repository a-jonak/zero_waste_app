from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create_account/', views.add_new_user, name='create_account'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_list/add_product', views.add_new_user_product, name='add_new_user_product'),
    path('product_list/add=<int:product_id>', views.add_user_product, name='add_user_product'),
    path('product_list/sub=<int:product_id>', views.sub_user_product, name='sub_user_product'),
    path('product_list/delete=<int:product_id>', views.delete_user_product, name='delete_user_product'),
    path('product_list/change=<int:product_id>', views.change_user_product, name='change_user_product'),
    path('product_list/shopping_list=<int:product_id>', views.add_product_to_shopping_list, name='add_product_to_shopping_list'),
    path('recipes/', views.RecipesView.as_view(), name='recipes'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('recipes/shopping_list=<int:product_id>', views.add_ingredient_to_shopping_list, name='add_ingredient_to_shopping_list'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list/add_product', views.add_new_shopping_product, name='add_new_shopping_product'),
    path('shopping_list/add=<int:product_id>', views.add_shopping_product, name='add_shopping_product'),
    path('shopping_list/sub=<int:product_id>', views.sub_shopping_product, name='sub_shopping_product'),
    path('shopping_list/delete=<int:product_id>', views.delete_shopping_product, name='delete_shopping_product'),
]