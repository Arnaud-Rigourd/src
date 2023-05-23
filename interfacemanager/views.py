from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from interfacemanager.models import FAQClient, FAQDev


User = get_user_model()

class FAQHome(TemplateView):
    template_name = 'interfacemanager/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['current_user'] = current_user
        if current_user.is_authenticated and hasattr(current_user, 'profile'):
            context['slug'] = current_user.slug
        context['faq_clients'] = FAQClient.objects.all()
        context['faq_devs'] = FAQDev.objects.all()
        return context
