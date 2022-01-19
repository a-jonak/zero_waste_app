import datetime

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from .models import User


class AddUserProductForm(forms.Form):
    product_name = forms.CharField(label='Nazwa produktu')
    number = forms.IntegerField(label='Ilość',initial=1, widget=forms.NumberInput())
    expiration_date = forms.DateField(label='Data ważności',  widget=forms.SelectDateWidget())

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        if data < datetime.date.today():
            raise ValidationError('Niepoprawna data - produkt po dacie ważności')
        return data


class AddUserForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', help_text='Wprowadź nazwę użytkownika')
    email = forms.EmailField(label='Adres email', help_text='Wprowadź adres email')
    password = forms.CharField(label='Hasło', help_text='Wprowadź hasło', widget=forms.PasswordInput())

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            user = User.objects.get(username=data)
            raise ValidationError('Użytkownik o takiej nazwie już istnieje: {}'.format(data))
        except:
            return data

    def clean_password(self):
        data = self.cleaned_data['password']
        validate_password(data)
        return data


class ChangeUserProductForm(forms.Form):
    product_name = ''
    number = forms.IntegerField(label='Ilość', widget=forms.NumberInput())
    expiration_date = forms.DateField(label='Data ważności', widget=forms.SelectDateWidget())

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        if data < datetime.date.today():
            raise ValidationError('Niepoprawna data - produkt po dacie ważności')
        return data


class AddShoppingProductForm(forms.Form):
    product_name = forms.CharField(label='Nazwa produktu')
    amount = forms.IntegerField(label='Ilość', initial=1, widget=forms.NumberInput())
