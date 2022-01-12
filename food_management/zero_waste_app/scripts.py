from typing import Counter

from .models import RecipeIngredient, UserProduct, UserShoppingList

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
