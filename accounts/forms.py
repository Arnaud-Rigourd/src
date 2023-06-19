import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class CustomSignupForm(UserCreationForm):
    username = forms.CharField(
        error_messages={
            'required': 'Please enter a username',
            'invalid': 'Please enter a valid username',
            'unique': 'This username is already taken'
        },
        widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                      'placeholder': "Nom d'utilisateur*"})
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Prénom*"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Nom*"})
    )

    email = forms.EmailField(
        error_messages={
            'required': 'Please enter an email address',
            'invalid': 'Please enter a valid email address',
            'unique': 'This email address is already taken'
        },
        widget=forms.TextInput(attrs={'placeholder': 'email@example.com*'})
    )

    phone_number = forms.CharField(
        error_messages={
            'invalid': 'Please enter a valid phone number',
        },
        widget=forms.TextInput(attrs={'placeholder': 'Téléphone : XX XX XX XX XX'})
    )

    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Nom d'entreprise (facultatif)"})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe*"})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Confirmez votre mot de passe*"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].required = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError("Le nom d'utilisateur ne doit contenir que des lettres et des chiffres.")
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            raise ValidationError("Le numéro de téléphone ne doit contenir que des chiffres, et doit être sous le format '0600000000'.")
        return phone_number


    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'category',
            'phone_number',
            # 'phone_display',
            'company_name',
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
    )



class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        error_messages={
            'invalid': 'Please enter a valid image',
        }
    )


class CustomUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10)
    phone_display = forms.BooleanField(required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            raise ValidationError(
                "Le numéro de téléphone ne doit contenir que des chiffres, et doit être sous le format '0600000000'.")
        return phone_number


    def clean_phone_display(self):
        phone_display = self.cleaned_data.get('phone_display')
        if phone_display:
            return True
        return False

    class Meta:
        model = CustomUser
        fields = (
            'phone_number',
            'phone_display',
        )
