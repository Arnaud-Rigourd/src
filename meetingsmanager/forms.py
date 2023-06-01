from django import forms
from django_flatpickr.widgets import DateTimePickerInput

from meetingsmanager.models import Meetings


class CustomMeetingForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ['title', 'message', 'meeting_date']
        widgets = {
            'meeting_date': DateTimePickerInput(),
        }