from django.urls import path, include, re_path, reverse_lazy
from django.contrib.auth import views as auth_views

from accounts.views import signup, signin, signout, confirm_email, resend_email, update_profile_picture, \
    update_profile_info
import django.contrib.auth.urls

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('confirm_email/<str:token>/', confirm_email, name='confirm_email'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('user/update/picture/<slug:slug>/<int:pk>/', update_profile_picture, name='update_profile_picture'),
    path('user/update/profile-info/<slug:slug>/<int:pk>/', update_profile_info, name='update_profile_info'),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(
        template_name='registration/custom_password_reset_form.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
        email_template_name='registration/custom_password_reset_email.html'
    ), name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/custom_password_reset_done.html',
    ), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/custom_password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/custom_password_reset_complete.html',
    ), name='password_reset_complete'),
    path('resend_email/<str:email>/', resend_email, name='resend_email'),
]
