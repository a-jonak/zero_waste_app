from typing import Counter

from .models import Product, Recipe, RecipeIngredient, UserProduct, UserShoppingList
from .parse_fractions import parse_problematic_numbers


def recipes_per_user_products(user_products):
    wanted_products = [user_pr.product for user_pr in user_products]
    recipes_matching_user_products = RecipeIngredient.objects.filter(ingredient__in=wanted_products)
    recipes_with_most_nr_of_product_match = Counter([product.recipe for product in recipes_matching_user_products])
    return [recipe[0] for recipe in sorted(recipes_with_most_nr_of_product_match.items(), key=lambda x: x[1], reverse=True)][:3]


def create_new_user_product(user, form, product):
    product_instance = UserProduct()
    product_instance.user = user
    product_instance.product = product
    product_instance.number = form.cleaned_data['number']
    product_instance.expiration_date = form.cleaned_data['expiration_date']
    product_instance.save()


def create_new_shopping_product(user, form, product):
    product_instance = UserShoppingList()
    product_instance.user = user
    product_instance.product = product
    product_instance.amount = form.cleaned_data['amount']
    product_instance.save()


def add_to_shopping_list(request, product):
    try:
        product_in_sp = UserShoppingList.objects.get(product=product, user=request.user)
        product_in_sp.amount += 1
        product_in_sp.save()
    except:
        new_product_in_sp = UserShoppingList()
        new_product_in_sp.user = request.user
        new_product_in_sp.product = product
        new_product_in_sp.save()


def get_units_present_in_database():
    units = set(unit[0] for unit in RecipeIngredient.objects.values_list('unit'))
    return units


def add_new_recipe_to_database(recipe_name, ingredients, instructions):
    new_recipe = Recipe()
    new_recipe.name = recipe_name
    new_recipe.instructions = instructions
    new_recipe.save()
    for ingredient in ingredients.split('\n'):
        name, amount, unit = ingredient.split(', ')
        ingredient_name = name.split(': ')[1]
        ingredient_amount = parse_problematic_numbers(amount.split(': ')[1])
        ingredient_unit = unit.split(': ')[1]
        try:
            product = Product.objects.get(name=ingredient_name)
        except:
            product = Product()
            product.name = ingredient_name
            product.save()
        recipe_ingredient = RecipeIngredient()
        recipe_ingredient.recipe = new_recipe
        recipe_ingredient.ingredient = product
        recipe_ingredient.amount = ingredient_amount
        recipe_ingredient.unit = ingredient_unit
        recipe_ingredient.save()
    return new_recipe
