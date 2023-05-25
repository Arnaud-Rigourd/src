from django import forms
from django.forms.models import inlineformset_factory
from .models import Profile, Stacks, Projects


class CustomProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'job']
        labels = {
            'description': 'Présente toi en quelques mots',
            'job': "Domaine d'expertise",
        }


class CustomStacksForm(forms.ModelForm):
    class Meta:
        model = Stacks
        fields = ['name']
        labels = {
            'name': 'Stacks',
        }


class CustomProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        fields = ['name', 'description', 'used_stacks', 'link']
        labels = {
            'name': 'Nom du projet',
            'description': 'Description',
            'used_stacks': 'Stacks utilisées',
            'link': 'Lien vers le projet',
        }



CustomStacksFormSet = inlineformset_factory(Profile, Stacks, form=CustomStacksForm, extra=1, can_delete=False)
CustomProjectsFormSet = inlineformset_factory(Profile, Projects, form=CustomProjectsForm, extra=1, can_delete=False)
