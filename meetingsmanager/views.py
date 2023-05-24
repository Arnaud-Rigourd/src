from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class MeetingsView(TemplateView):
    template_name = "meetingsmanager/test.html"