from django import forms

from meetingsmanager.models import Meetings


class CustomMeetingForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ['title', 'message', 'meeting_date']