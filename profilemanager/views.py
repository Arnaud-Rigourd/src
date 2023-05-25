from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from accounts.forms import CustomUpdateForm
from meetingsmanager.forms import CustomMeetingForm
from profilemanager.forms import CustomProfileForm, CustomStacksFormSet, CustomProjectsFormSet, CustomStacksForm, \
    CustomProjectsForm
from profilemanager.models import Profile, Stacks, Projects, Company

User = get_user_model()


# Profile management
class ProfileIndex(TemplateView):
    template_name = "profilemanager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['current_user'] = self.request.user
        context['devs'] = User.objects.filter(category='developpeur')
        return context


class ProfileDetail(TemplateView):
    template_name = "profilemanager/detail.html"

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.kwargs['pk'], user__slug=self.kwargs['slug'])
        if profile:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)

        context['user'] = user
        context['current_user'] = self.request.user
        context['slug'] = slug
        context['pk'] = pk
        context['profile'] = user.profile
        context['dev'] = user.category == 'developpeur'
        context['stacks'] = user.profile.stacks_set.all()
        context['projects'] = user.profile.projects_set.all()
        context['stack_form'] = CustomStacksForm()
        context['project_form'] = CustomProjectsForm()
        context['profile_form'] = CustomUpdateForm()
        context['user_form'] = CustomUpdateForm()
        context['not_phone_display'] = not user.phone_display
        context['meeting_form'] = CustomMeetingForm()

        return context

# dispatch method overloaded to check if the user is the owner of the profile
class ProfileUpdate(UpdateView):
    template_name = "profilemanager/update.html"
    model = Profile
    form_class = CustomProfileForm

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user != profile.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['profile_pk'] = self.kwargs['pk']
        context['current_user'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.profile = self.request.user.profile
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileCreate(CreateView):
    template_name = "profilemanager/create.html"
    form_class = CustomProfileForm

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        if self.request.POST:
            context['stacks'] = CustomStacksFormSet(self.request.POST)
            context['projects'] = CustomProjectsFormSet(self.request.POST)
        else:
            context['current_user'] = self.request.user
            context['stacks'] = CustomStacksFormSet()
            context['projects'] = CustomProjectsFormSet()
        return context

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


# Stacks management
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

        if self.request.headers.get('HX-Request'):
            html = render_to_string('profilemanager/partials/stacks_partial.html', {'stack': self.object})
            return HttpResponse(html)
        return super().form_valid(form)

# dispatch method overloaded to check if the user is the owner of the profile
class StackUpdate(UpdateView):
    template_name = "profilemanager/detail.html"
    model = Stacks
    fields = ['name']

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug != self.kwargs['slug']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.profile = self.request.user.profile
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        self.object.save()

        if self.request.headers.get('HX-Request'):
            html = render_to_string('profilemanager/partials/stacks_partial.html', {'stack': self.object})
            return HttpResponse(html)
        return super().form_valid(form)

# dispatch method overloaded to check if the user is the owner of the profile
class StackDelete(DeleteView):
    template_name = "profilemanager/detail.html"
    model = Stacks

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug != self.kwargs['slug']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        stack_id = self.kwargs['pk']
        stack = get_object_or_404(Stacks, pk=stack_id)
        stack.delete()

        if self.request.headers.get('HX-Request'):
            return HttpResponse('')
        return super().post(request, *args, **kwargs)


# Projects management
@method_decorator(login_required, name='dispatch')
class ProjectCreate(CreateView):
    template_name = "profilemanager/detail.html"
    model = Projects
    fields = ['name', 'description', 'used_stacks', 'link']

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.profile = self.request.user.profile
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        self.object.save()
        return super().form_valid(form)

# dispatch method overloaded to check if the user is the owner of the profile
class ProjectUpdate(UpdateView):
    template_name = "profilemanager/projects/edit.html"
    model = Projects
    fields = ['name', 'description', 'used_stacks', 'link']

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug != self.kwargs['slug']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['current_user'] = current_user
        context['slug'] = current_user.slug
        context['pk'] = self.kwargs['pk']
        return context
    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.profile = self.request.user.profile
        except ObjectDoesNotExist:
            return self.form_invalid(form)
        self.object.save()
        return super().form_valid(form)

# dispatch method overloaded to check if the user is the owner of the profile
class ProjectDelete(DeleteView):
    template_name = "profilemanager/detail.html"
    model = Projects

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug != self.kwargs['slug']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profilemanager:detail', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.pk})

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        try:
            project = Projects.objects.get(pk=project_id)
        except Projects.DoesNotExist:
            return HttpResponse("Project does not exist.")
        else:
            project.delete()
            return super().get(request, *args, **kwargs)


class CompanyDetail(TemplateView):
    template_name = "profilemanager/company/detail.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.category != 'company' or request.user.pk != self.kwargs['pk']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        company = get_object_or_404(Company, user__pk=self.kwargs['pk'])

        context['company'] = company
        context['meetings'] = company.meetings_set.all()

        context['user'] = user
        context['current_user'] = self.request.user
        return context


class ProfileMeetings(TemplateView):
    template_name = "profilemanager/my_meetings.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.kwargs['pk']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        current_user = self.request.user
        context['current_user'] = current_user
        context['user'] = user
        context['meetings'] = user.profile.meetings_set.all()
        context['meeting_form'] = CustomMeetingForm()
        return context



