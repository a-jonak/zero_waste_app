import datetime

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class AddProductForm(forms.Form):
    product_name = forms.CharField(help_text='Enter product name')
    number = forms.IntegerField(initial=1)
    expiration_date = forms.DateField(help_text='Enter product expiration date')

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        if data < datetime.date.today():
            raise ValidationError('Invalid date - product past expiration date')
        return data


class AddUserForm(forms.Form):
    user_name = forms.CharField(help_text='Enter user name')
    email = forms.EmailField(help_text='Enter email')
    password = forms.CharField(help_text='Enter password', widget=forms.PasswordInput())

    def clean_password(self):
        data = self.cleaned_data['password']
        validate_password(data)
        return data

