from django.urls import path

from meetingsmanager.views import MeetingsView

app_name = 'meetingsmanager'

urlpatterns = [
    path('meetings/', MeetingsView.as_view(), name="test"),
]