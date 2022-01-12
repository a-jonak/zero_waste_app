import datetime

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class AddUserProductForm(forms.Form):
    product_name = forms.CharField(help_text='Nazwa produktu')
    number = forms.IntegerField(initial=1, widget=forms.NumberInput())
    expiration_date = forms.DateField(help_text='Data ważności',  widget=forms.SelectDateWidget())

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        if data < datetime.date.today():
            raise ValidationError('Niepoprawna data - produkt po dacie ważności')
        return data


class AddUserForm(forms.Form):
    user_name = forms.CharField(help_text='Wprowadź nazwę użytkownika')
    email = forms.EmailField(help_text='Wprowadź adres email')
    password = forms.CharField(help_text='Wprowadź hasło', widget=forms.PasswordInput())

    def clean_password(self):
        data = self.cleaned_data['password']
        validate_password(data)
        return data


class ChangeUserProductForm(forms.Form):
    product_name = ''
    number = forms.IntegerField(widget=forms.NumberInput())
    expiration_date = forms.DateField(widget=forms.SelectDateWidget())

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        if data < datetime.date.today():
            raise ValidationError('Niepoprawna data - produkt po dacie ważności')
        return data


class AddShoppingProductForm(forms.Form):
    product_name = forms.CharField(help_text='Nazwa produktu')
    amount = forms.IntegerField(initial=1, widget=forms.NumberInput())
