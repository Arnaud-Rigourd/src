import re

from django.contrib.auth.forms import UserCreationForm
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
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    email = forms.EmailField(
        error_messages={
            'required': 'Please enter an email address',
            'invalid': 'Please enter a valid email address',
            'unique': 'This email address is already taken'
        }
    )

    phone_number = forms.CharField(
        error_messages={
            'invalid': 'Please enter a valid phone number',
        }
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'category',
            'phone_number',
            'phone_display',
            'company_name',
        )


class CustomLoginForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter an email address',
            'invalid': 'Please enter a valid email address'
        }
    )
    class Meta:
        model = CustomUser
        fields = (
            'email',
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
        phone_number = re.sub('[^0-9]', '', self.cleaned_data.get('phone_number'))
        if len(phone_number) == 10 and phone_number.isdigit():
            return phone_number
        raise ValidationError("Le numéro de téléphone doit être composé d'exactement 10 chiffres.")


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
