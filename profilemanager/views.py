from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView

from profilemanager.forms import CustomProfileForm, CustomStacksFormSet, CustomProjectsFormSet, CustomStacksForm, \
    CustomProjectsForm
from profilemanager.models import Profile, Stacks, Projects

User = get_user_model()


class ProfileDetail(TemplateView):
    template_name = "profilemanager/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            context['error_message'] = f"No user with username {username} exists."
        else:
            context['user'] = user
            context['current_user'] = self.request.user
            context['username'] = username
            context['profile'] = user.profile
            context['stacks'] = user.profile.stacks_set.all()
            context['projects'] = user.profile.projects_set.all()
            context['stack_form'] = CustomStacksForm()
            context['project_form'] = CustomProjectsForm()
        return context


@method_decorator(login_required, name='dispatch')
class ProfileCreate(CreateView):
    template_name = "profilemanager/create.html"
    form_class = CustomProfileForm

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['stacks'] = CustomStacksFormSet(self.request.POST)
            data['projects'] = CustomProjectsFormSet(self.request.POST)
        else:
            data['current_user'] = self.request.user
            data['stacks'] = CustomStacksFormSet()
            data['projects'] = CustomProjectsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        stacks = context['stacks']
        projects = context['projects']
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if stacks.is_valid() and projects.is_valid():
            stacks.instance = self.object
            stacks.save()
            projects.instance = self.object
            projects.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class StackCreate(CreateView):
    template_name = "profilemanager/detail.html"
    model = Stacks
    fields = ['name']

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.profile = self.request.user.profile
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        self.object.save()
        return super().form_valid(form)


class ProjectCreate(CreateView):
    template_name = "profilemanager/detail.html"
    model = Projects
    fields = ['name', 'description', 'used_stacks', 'link']

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.profile = self.request.user.profile
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        self.object.save()
        return super().form_valid(form)
