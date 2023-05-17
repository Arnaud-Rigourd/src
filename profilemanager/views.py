from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

User = get_user_model()


class ProfileDetail(TemplateView):
    template_name = "profilemanager/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            context['error_message'] = f"No user with username {username} exists."
        else:
            context['user'] = user
            context['username'] = username
            context['profile'] = user.profile
            context['stacks'] = user.profile.stacks_set.all()
            context['projects'] = user.profile.projects_set.all()
        return context
