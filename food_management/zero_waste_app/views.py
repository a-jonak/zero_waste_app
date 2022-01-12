from datetime import date
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import AddShoppingProductForm, AddUserForm, AddUserProductForm, ChangeUserProductForm
from .models import Product, Recipe, RecipeIngredient, UserProduct, UserShoppingList
from .scripts import add_to_shopping_list, create_new_shopping_product, create_new_user_product, recipes_per_user_products


def index(request):
    recipes = Recipe.objects.all()
    random_indexes = random.sample(range(1, len(recipes)), 5)
    example_recipes = Recipe.objects.filter(pk__in=random_indexes)
    return render(request, 'zero_waste_app/index.html', {'example_recipes': example_recipes})


@login_required
def product_list(request):
    userproduct_list = UserProduct.objects.filter(user=request.user)
    recipes = recipes_per_user_products(userproduct_list)
    return render(request, 'zero_waste_app/product_list.html', {'userproduct_list': userproduct_list, 'mached_recipes': recipes})


@login_required
def recipe(request, recipe_id):
    r = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe_id)
    return render(request, 'zero_waste_app/recipe.html', {
        'name': r.name,
        'ingredients_list': ingredients,
        'instruction': r.instructions
    })


@login_required
def shopping_list(request):
    shopping_list = UserShoppingList.objects.filter(user=request.user)
    return render(request, 'zero_waste_app/shopping_list.html', {'shopping_list': shopping_list})


class RecipesView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'zero_waste_app/recipes.html'
    paginate_by = 20


def add_new_user_product(request):
    if request.method == 'POST':
        form = AddUserProductForm(request.POST)
        if form.is_valid():
            try:
                product_in_database = Product.objects.get(name=form.cleaned_data['product_name'])
                create_new_user_product(request.user, form, product_in_database)
            except:
                product = Product()
                product.name = form.cleaned_data['product_name']
                product.save()
                create_new_user_product(request.user, form, product)

            return redirect('product_list')
    else:
        initial = {
            'product_name': '',
            'expiration_date': date.today()
        }
        form = AddUserProductForm(initial=initial)
    return render(request, 'zero_waste_app/add_new_user_product.html', { 'form': form })


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
            return redirect('login')
    else:
        form = AddUserForm()
    return render(request, 'zero_waste_app/add_new_user.html', {'form': form})


def add_user_product(request, product_id):
    product_object = UserProduct.objects.get(pk=product_id)
    product_object.number += 1
    product_object.save()
    return redirect('product_list')


def sub_user_product(request, product_id):
    product_object = UserProduct.objects.get(pk=product_id)
    product_object.number -= 1
    product_object.save()
    return redirect('product_list')


def delete_user_product(request, product_id):
    product_object = UserProduct.objects.get(pk=product_id)
    product_object.delete()
    return redirect('product_list')


def change_user_product(request, product_id):
    product_object = UserProduct.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ChangeUserProductForm(request.POST)
        if form.is_valid():
            product_object.number = form.cleaned_data['number']
            product_object.expiration_date = form.cleaned_data['expiration_date']
            product_object.save()
            return redirect('product_list')
    else:
        initial = {
            'product_name': product_object.product.name,
            'number': product_object.number,
            'expiration_date': product_object.expiration_date
        }
        form = ChangeUserProductForm(initial=initial)
    return render(request, 'zero_waste_app/change_user_product.html', { 'product_name': product_object.product.name, 'form': form })


def add_shopping_product(request, product_id):
    product_object = UserShoppingList.objects.get(pk=product_id)
    product_object.amount += 1
    product_object.save()
    return redirect('shopping_list')


def sub_shopping_product(request, product_id):
    product_object = UserShoppingList.objects.get(pk=product_id)
    product_object.amount -= 1
    product_object.save()
    return redirect('shopping_list')


def delete_shopping_product(request, product_id):
    product_object = UserShoppingList.objects.get(pk=product_id)
    product_object.delete()
    return redirect('shopping_list')


def add_new_shopping_product(request):
    if request.method == 'POST':
        form = AddShoppingProductForm(request.POST)
        if form.is_valid():
            try:
                product_in_database = Product.objects.get(name=form.cleaned_data['product_name'])
                create_new_shopping_product(request.user, form, product_in_database)
            except:
                product = Product()
                product.name = form.cleaned_data['product_name']
                product.save()
                create_new_shopping_product(request.user, form, product)

            return redirect('shopping_list')
    else:
        initial = {
            'product_name': '',
        }
        form = AddShoppingProductForm(initial=initial)
    return render(request, 'zero_waste_app/add_new_user_product.html', { 'form': form })


def add_product_to_shopping_list(request, product_id):
    user_product = UserProduct.objects.get(pk=product_id)
    add_to_shopping_list(request, user_product.product)
    return redirect('product_list')


def add_ingredient_to_shopping_list(request, product_id):
    recipe_ingredient = RecipeIngredient.objects.get(pk=product_id)
    add_to_shopping_list(request, recipe_ingredient.ingredient)
    return redirect('recipe', recipe_id=recipe_ingredient.recipe.id)
