from datetime import date
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import AddRecipeForm, AddShoppingProductForm, AddUserProductForm, ChangeUserProductForm, CustomUserCreationForm
from .models import Product, Recipe, RecipeIngredient, UserProduct, UserShoppingList
from .scripts import (add_new_recipe_to_database, add_to_shopping_list, create_new_shopping_product, create_new_user_product,
recipes_per_user_products, get_units_present_in_database)
from .parse_recipe import get_recipe_informations


def index(request):
    recipes = Recipe.objects.all()
    example_recipes = []
    if len(recipes) > 0:
        example_recipes = [recipes[index] for index in random.sample(range(0, len(recipes)), 5)]
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'zero_waste_app/add_new_user.html', {'form': form})


def update_user_product(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        action = request.GET['action']
        product_object = UserProduct.objects.get(pk=product_id)
        
        if action == 'add':
            product_object.number += 1
        elif action == 'sub':
            product_object.number -= 1
        product_object.save()
        if product_object.number <= 0:
            product_object.delete()
    return JsonResponse(product_object.number, safe=False)


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


def update_shopping_product(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        action = request.GET['action']
        product_object = UserShoppingList.objects.get(pk=product_id)
        
        if action == 'add':
            product_object.amount += 1
        elif action == 'sub':
            product_object.amount -= 1
        product_object.save()
        if product_object.amount <= 0:
            product_object.delete()
    return JsonResponse(product_object.amount, safe=False)


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
    return render(request, 'zero_waste_app/add_new_shopping_product.html', { 'form': form })


def add_product_to_shopping_list(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product_object = Product.objects.get(pk=product_id)
        add_to_shopping_list(request, product_object)
    return JsonResponse("Dodano do listy zakup??w", safe=False)


def add_recipe(request):
    if request.method == 'GET':
        page_url = request.GET['recipe_url']
        units = get_units_present_in_database()
        name, ingredients, instructions = get_recipe_informations(page_url, units)
        return JsonResponse({'name': name, 'ingredients': ingredients, 'instructions': instructions})


@login_required
def add_new_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            recipe = add_new_recipe_to_database(form.cleaned_data['recipe_name'], form.cleaned_data['recipe_ingredients'],
                                                form.cleaned_data['recipe_instructions'])
            return redirect('recipe', recipe_id=recipe.id)
    else:
        initial = {
            'recipe_name': '',
            'ingredients': '',
            'instructions': ''
        }
        form = AddRecipeForm(initial=initial)

    return render(request, 'zero_waste_app/add_new_recipe.html', {'form': form})
