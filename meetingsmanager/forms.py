from django import forms
from django_flatpickr.widgets import DateTimePickerInput

from meetingsmanager.models import Meetings


class CustomMeetingForm(forms.ModelForm):
    meeting_date = forms.DateTimeField(
        widget=DateTimePickerInput()
    )

    class Meta:
        model = Meetings
        fields = ['title', 'message', 'meeting_date']
        widgets = {
            'meeting_date': DateTimePickerInput(),
        }