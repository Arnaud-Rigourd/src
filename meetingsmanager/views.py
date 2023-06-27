from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from devforfree import settings
from meetingsmanager.forms import CustomMeetingForm, CustomMessageFormSet, CustomMessageForm
from meetingsmanager.models import Meetings, Messages
from profilemanager.models import Company, Profile

User = get_user_model()


class MeetingsCreate(CreateView):
    template_name = "profilemanager/detail.html"
    form_class = CustomMeetingForm

    def get_success_url(self):
        return reverse('profilemanager:company-monitoring',
                       kwargs={'slug': self.object.company.user.slug, 'pk': self.object.company.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['messages'] = CustomMessageFormSet(self.request.POST)
        else:
            context['current_user'] = self.request.user
            context['messages'] = CustomMessageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        message_form = context['messages']
        self.object = form.save(commit=False)
        self.object.dev = get_object_or_404(Profile, pk=self.kwargs['dev_pk'])
        self.object.company = get_object_or_404(Company, pk=self.kwargs['company_pk'])
        self.object.save()

        if message_form.is_valid():
            for message in message_form:
                message = message.save(commit=False)
                message.meeting = self.object
                message.sender = get_object_or_404(User, pk=self.request.user.pk)
                message.receiver = get_object_or_404(User, pk=message.meeting.dev.user_id)
                message.save()

        subject, message, email_from, email_to = first_email_content(self, self.object)
        send_mail(subject, message, email_from, email_to)
        return super().form_valid(form)


class MeetingsIndex(TemplateView):
    template_name = "profilemanager/company/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, user__pk=self.kwargs['pk'])
        context['company'] = company
        context['meetings'] = company.meetings_set.all()
        return context


class MeetingsUpdate(UpdateView):
    template_name = "profilemanager/company/detail.html"
    model = Meetings
    fields = ['status']
    pk_url_kwarg = 'meeting_pk'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        meeting = self.get_object()
        if request.user.pk != meeting.dev.user.pk:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profilemanager:dev-meetings',
                       kwargs={'pk': self.request.user.pk, 'slug': self.request.user.slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        meeting = get_object_or_404(Meetings, pk=self.kwargs['meeting_pk'])
        try:
            self.object.dev = meeting.dev
            self.object.company = meeting.company
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        self.object.save()
        return super().form_valid(form)


class MeetingsDelete(DeleteView):
    template_name = 'profilemanager/company/detail.html'
    model = Meetings
    pk_url_kwarg = 'meeting_pk'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        meeting = self.get_object()
        if request.user.pk != meeting.company.user.pk:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profilemanager:company-monitoring',
                       kwargs={'slug': self.object.company.user.slug, 'pk': self.object.company.user.pk})


class MessagesCreate(CreateView):
    template_name = 'profilemanager/my_meetings.html'
    form_class = CustomMessageForm

    def get_success_url(self):
        if self.request.user.category == 'company':
            return reverse('profilemanager:company-monitoring',
                           kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})
        elif self.request.user.category == 'developpeur':
            return reverse('profilemanager:dev-meetings',
                           kwargs={'pk': self.request.user.pk, 'slug': self.request.user.slug})
        else:
            return reverse('interfacemanager:home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        meeting = get_object_or_404(Meetings, pk=self.kwargs['meeting_pk'])
        sender = get_object_or_404(User, pk=self.request.user.pk)
        if sender == meeting.company.user:
            receiver = get_object_or_404(User, pk=meeting.dev.user_id)
        else:
            receiver = get_object_or_404(User, pk=meeting.company.user_id)

        self.object.sender = sender
        self.object.receiver = receiver
        self.object.meeting = meeting

        self.object.save()
        subject, message, email_from, email_to = _email_content(self, self.object)
        send_mail(subject, message, email_from, email_to)
        return super().form_valid(form)


def first_email_content(self, object):
    subject = self.object.title
    message = render_to_string('meetingsmanager/email.html',
                               {'company': self.object.company, 'dev': self.object.dev, 'meeting': self.object})
    email_from = settings.EMAIL_HOST_USER
    email_to = [object.dev.user.email]
    return subject, message, email_from, email_to


def _email_content(self, object):
    subject = f"Nouveau message de {object.sender.first_name} !"
    message = render_to_string('meetingsmanager/email_exchanges.html', {'sender': object.sender, 'object': object})
    email_from = settings.EMAIL_HOST_USER
    email_to = [object.receiver.email]
    return subject, message, email_from, email_to
