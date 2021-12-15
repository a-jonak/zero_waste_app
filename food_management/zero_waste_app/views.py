from datetime import date, datetime
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
from .models import ProductInstance, Recipe


class IndexView(generic.TemplateView):
    template_name = 'zero_waste_app/index.html'


# @login_required
# def product_list(request, user_id):
#     products = ProductInstance.objects.filter(user=user_id)
#     # return HttpResponse("You're looking at product list of: {}".format(user_id))
#     return render(request, 'zero_waste_app/product_list.html', { 'product_list': products })
class ProductListView(LoginRequiredMixin, generic.ListView):
    model = ProductInstance
    template_name = 'zero_waste_app/product_list.html'

    def get_queryset(self):
        return ProductInstance.objects.filter(user=self.request.user)

@login_required
def recipe(request, recipe_id):
    r = get_object_or_404(Recipe, pk=recipe_id)
    ingredients_list = [ingredient for ingredient in r.ingredients.split('\n')]
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
    paginate_by = 10


def add_new_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product_instance = ProductInstance()
            product_instance.user = request.user
            product_instance.product = form.cleaned_data['product_name']
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
