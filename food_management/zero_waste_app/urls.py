from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_account/', views.add_new_user, name='create_account'),
    # path('product_list/', views.ProductListView.as_view(), name='product_list'),
    # path('<int:user_id>/product_list/', views.product_list, name='product_list'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_list/add_product', views.add_new_user_product, name='add_new_user_product'),
    path('product_list/add=<int:product_id>', views.add_user_product, name='add_user_product'),
    path('product_list/sub=<int:product_id>', views.sub_user_product, name='sub_user_product'),
    path('product_list/delete=<int:product_id>', views.delete_user_product, name='delete_user_product'),
    path('product_list/change=<int:product_id>', views.change_user_product, name='change_user_product'),
    path('recipes/', views.RecipesView.as_view(), name='recipes'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list/add_product', views.add_new_shopping_product, name='add_new_shopping_product'),
    path('shopping_list/add=<int:product_id>', views.add_shopping_product, name='add_shopping_product'),
    path('shopping_list/sub=<int:product_id>', views.sub_shopping_product, name='sub_shopping_product'),
    path('shopping_list/delete=<int:product_id>', views.delete_shopping_product, name='delete_shopping_product'),
]