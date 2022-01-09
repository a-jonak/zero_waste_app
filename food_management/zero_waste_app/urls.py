from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('product_list/', views.product_list, name='product_list'),
    # path('<int:user_id>/product_list/', views.product_list, name='product_list'),
    path('recipes/', views.RecipesView.as_view(), name='recipes'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('product_list/add_product', views.add_new_product, name='add_new_product'),
    path('create_account/', views.add_new_user, name='create_account'),
]