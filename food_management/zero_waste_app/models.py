from django.contrib.auth.models import User
from django.db import models
from datetime import date, timedelta


# class User(models.Model):
#     name = models.CharField(max_length=50, help_text='Enter your desired user name')
#     password = models.CharField(max_length=50, help_text='Enter password')
        
#     def __str__(self) -> str:
#         return self.name


class ProductInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    number = models.IntegerField(default=1)
    expiration_date = models.DateField()

    @property
    def has_short_expiration_date(self):
        return self.expiration_date - date.today() < timedelta(days=3)

    class Meta:
        permissions = (('can_add_new_product', 'Add new product'),
                       ('can_add_existing_product', 'Add product'),
                       ('can_delete_product', 'Delete product'),)

    def __str__(self) -> str:
        return self.product


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
