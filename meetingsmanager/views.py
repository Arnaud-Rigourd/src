from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from meetingsmanager.forms import CustomMeetingForm
from profilemanager.models import Company, Profile


User = get_user_model()
class MeetingsCreate(CreateView):
    template_name = "profilemanager/detail.html"
    form_class = CustomMeetingForm

    def get_success_url(self):
        return reverse('interfacemanager:home')

    def form_valid(self, form):
        print('form_valid')
        self.object = form.save(commit=False)
        self.object.dev = get_object_or_404(Profile, pk=self.kwargs['dev_pk'])
        self.object.company = get_object_or_404(Company, pk=self.kwargs['company_pk'])
        self.object.save()
        return super().form_valid(form)


class MeetingsIndex(TemplateView):
    template_name = "profilemanager/company/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, user__pk=self.kwargs['pk'])
        context['company'] = company
        context['meetings'] = company.meetings_set.all()
        return context
