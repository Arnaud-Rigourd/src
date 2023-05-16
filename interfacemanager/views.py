from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from interfacemanager.models import FAQClient, FAQDev


class FAQHome(TemplateView):
    templates_name = 'interfacemanager/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_clients'] = FAQClient.objects.all()
        context['faq_devs'] = FAQDev.objects.all()
        return context
