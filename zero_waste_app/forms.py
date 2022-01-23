import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', min_length=4, max_length=150)
    email = forms.EmailField(label='Adres email', widget=forms.EmailInput)
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Użytkownik o takiej nazwie już istnieje")
        return username
    
    def clean_password1(self):
        data = self.cleaned_data['password1']
        try:
            validate_password(data)
            return data
        except:
            raise ValidationError("To hasło jest zbyt krótkie. Musi zawierać co najmniej 8 znaków."
                                  "To hasło jest zbyt proste.")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Hasło się nie zgadza")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class AddUserProductForm(forms.Form):
    product_name = forms.CharField(label='Nazwa produktu')
    number = forms.IntegerField(label='Ilość',initial=1, widget=forms.NumberInput())
    expiration_date = forms.DateField(label='Data ważności',  widget=forms.SelectDateWidget())

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        if data < datetime.date.today():
            raise ValidationError('Niepoprawna data - produkt po dacie ważności')
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


class AddRecipeForm(forms.Form):
    recipe_name = forms.CharField(label='Nazwa przepisu')
    recipe_ingredients = forms.CharField(label='Składniki', widget=forms.TextInput())
    recipe_instructions = forms.CharField(label='Sposób przygotowania', widget=forms.TextInput())
