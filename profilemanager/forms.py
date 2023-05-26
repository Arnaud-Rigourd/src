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
        fields = ['name', 'link', 'description', 'used_stacks']
        labels = {
            'name': 'Nom du projet',
            'link': 'Lien vers le projet',
            'description': 'Description',
            'used_stacks': 'Stacks utilisées',
        }

    def __init__(self, *args, **kwargs) -> None:
        """
        Filter the 'used_stacks' field's queryset to only include Stacks that are related to the given user's profile and exclude the JSON remaining stack.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            user: The User instance used for filtering the 'used_stacks' queryset.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['used_stacks'].queryset = Stacks.objects.filter(profile__user=user).exclude(name__startswith='[{')



CustomStacksFormSet = inlineformset_factory(Profile, Stacks, form=CustomStacksForm, extra=1, can_delete=False)
CustomProjectsFormSet = inlineformset_factory(Profile, Projects, form=CustomProjectsForm, extra=1, can_delete=False)
