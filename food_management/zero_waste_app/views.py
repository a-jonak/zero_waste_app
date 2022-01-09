from datetime import date, datetime
from typing import Counter
from django.contrib.auth.models import Group, User
from django.db import reset_queries
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import AddProductForm, AddUserForm
from .models import Product, Recipe, RecipeIngredient, UserProduct


class IndexView(generic.TemplateView):
    template_name = 'zero_waste_app/index.html'


# @login_required
# def product_list(request, user_id):
#     products = ProductInstance.objects.filter(user=user_id)
#     # return HttpResponse("You're looking at product list of: {}".format(user_id))
#     return render(request, 'zero_waste_app/product_list.html', { 'product_list': products })
# class ProductListView(LoginRequiredMixin, generic.ListView):
#     model = ProductInstance
#     template_name = 'zero_waste_app/product_list.html'

#     def get_queryset(self):
#         return ProductInstance.objects.filter(user=self.request.user)
# class ProductListView(LoginRequiredMixin, generic.ListView):
#     model = UserProduct
#     template_name = 'zero_waste_app/product_list.html'
#     context['recipes'] = recipes_per_user_products()

#     def get_queryset(self):
#         return UserProduct.objects.filter(user=self.request.user)
    
#     def recipes_per_user_products(self):
#         user_products = UserProduct.objects.filter(user=self.request.user)
#         recipes_matching_user_products = RecipeIngredient.objects.filter(ingredient__in=user_products)
#         recipes_with_most_nr_of_product_match = Counter(recipes_matching_user_products).keys()[:3]
#         return recipes_with_most_nr_of_product_match

@login_required
def product_list(request):
    userproduct_list = UserProduct.objects.filter(user=request.user)
    recipes = recipes_per_user_products(userproduct_list)
    return render(request, 'zero_waste_app/product_list.html', {'userproduct_list': userproduct_list, 'mached_recipes': recipes})


@login_required
def recipe(request, recipe_id):
    r = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe_id)
    ingredients_list = [product for product in ingredients]
    return render(request, 'zero_waste_app/recipe.html', {
        'name': r.name,
        'ingredients_list': ingredients_list,
        'instruction': r.instructions
    })


# class RecipeView(generic.DetailView):
#     model = Recipe
#     ingredient_list = [ing for ing in Recipe.ingredients.split('\n')]
#     # context_object_name = 'ingredients_list'
#     template_name = 'zero_waste_app/recipe.html'
    # def get_queryset(self):
    #     return [ingredient for ingredient in Recipe.ingredients.split('\n')]

# def recipes(request):
#     recipes_list = Recipe.objects.all
#     return render(request, 'zero_waste_app/recipes.html', { 'recipes_list': recipes_list })
class RecipesView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'zero_waste_app/recipes.html'
    paginate_by = 20


def add_new_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            try:
                product_in_database = Product.objects.get(name=form.cleaned_data['product_name'])
                product_instance = UserProduct()
                product_instance.user = request.user
                product_instance.product = product_in_database
                product_instance.number = form.cleaned_data['number']
                product_instance.expiration_date = form.cleaned_data['expiration_date']
                product_instance.save()
            except:
                product = Product()
                product.name = form.cleaned_data['product_name']
                product.save()
                product_instance = UserProduct()
                product_instance.user = request.user
                product_instance.product = product
                product_instance.number = form.cleaned_data['number']
                product_instance.expiration_date = form.cleaned_data['expiration_date']
                product_instance.save()

            return HttpResponseRedirect(reverse('product_list'))
    else:
        initial = {
            'product_name': '',
            'expiration_date': date.today()
        }
        form = AddProductForm(initial=initial)
    return render(request, 'zero_waste_app/add_new_product.html', { 'form': form })


# def add_product(request, pk):
#     product_instance = get_object_or_404(ProductInstance, pk=pk)
#     if request.method == 'POST':

def add_new_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['user_name'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
                )
            group = Group.objects.get(name='Zero Waste App users')
            group.user_set.add(user)
            user.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = AddUserForm()
    return render(request, 'zero_waste_app/add_new_user.html', {'form': form})


def recipes_per_user_products(user_products):
    # user_products = UserProduct.objects.filter(user=user)
    wanted_products = [user_pr.product for user_pr in user_products]
    recipes_matching_user_products = RecipeIngredient.objects.filter(ingredient__in=wanted_products)
    recipes_with_most_nr_of_product_match = Counter([product.recipe for product in recipes_matching_user_products])
    # print(recipes_with_most_nr_of_product_match)
    return [recipe[0] for recipe in sorted(recipes_with_most_nr_of_product_match.items(), key=lambda x: x[1], reverse=True)][:3]
