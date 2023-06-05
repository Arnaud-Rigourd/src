from django import forms
from django.forms import inlineformset_factory
from django_flatpickr.widgets import DateTimePickerInput

from meetingsmanager.models import Meetings, Messages


class CustomMeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].required = False
    class Meta:
        model = Meetings
        fields = ['title', 'message', 'meeting_date']
        widgets = {
            'meeting_date': DateTimePickerInput(),
        }


class CustomMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content']
        widgets = {
            'meeting_date': DateTimePickerInput(),
        }

CustomMessageFormSet = inlineformset_factory(Meetings, Messages, form=CustomMessageForm, extra=1, can_delete=False)
