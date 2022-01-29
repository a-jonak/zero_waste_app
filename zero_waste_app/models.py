from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE


class Product(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    expiration_date = models.DateField()

    @property
    def has_short_expiration_date(self):
        return timedelta(days=0) <= self.expiration_date - date.today() < timedelta(days=3)

    @property
    def after_expiration_date(self):
        return self.expiration_date - date.today() < timedelta(days=0)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    ingredient = models.ForeignKey(Product, on_delete=CASCADE)
    amount = models.FloatField()
    unit = models.TextField(default=0)


class UserShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    amount = models.IntegerField(default=1)
