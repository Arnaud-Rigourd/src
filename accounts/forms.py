from django.contrib.auth.forms import UserCreationForm
from django import forms

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

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
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
