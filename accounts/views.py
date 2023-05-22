import os

import cloudinary
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from dotenv import load_dotenv

from accounts.forms import CustomSignupForm, ImageUploadForm
from accounts.models import EmailConfirmation, CustomUser


def signup(request):
    context = {}
    if request.method == "POST":
        print('form submitted')
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            context = _send_confirmation_email(request, context, form)
            return render(request, 'registration/email_confirmation_done.html', context=context)
        else:
            context["errors"] = form.errors
    else:
        form = CustomSignupForm()

    context["form"] = form
    return render(request, "registration/signup.html", context=context)


def confirm_email(request, token):
    try:
        email_confirmation = EmailConfirmation.objects.get(token=token)
        user = email_confirmation.user
        user.is_active = True
        user.save()
        email_confirmation.delete()
        return render(request, 'registration/email_confirmation_success.html')
    except EmailConfirmation.DoesNotExist:
        return render(request, 'registration/email_confirmation_failed.html')


def resend_email(request, email):
    try:
        user = CustomUser.objects.get(email=email)
        email_confirmation = EmailConfirmation.objects.get(user=user)
    except (CustomUser.DoesNotExist, EmailConfirmation.DoesNotExist):
        messages.error(request, "User or email confirmation not found.")
        return redirect('accounts:signup')

    subject, message, from_email = _email_content(request, email_confirmation)
    send_mail(subject, message, from_email, [email])
    messages.success(request, "Email sent successfully. Please check your inbox.")
    return render(request, 'registration/email_confirmation_done.html', context={'user': user})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('interfacemanager:home')
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", context={'form': form})


def signout(request):
    logout(request)
    return redirect('interfacemanager:home')


def update_profile_picture(request, pk):
    context = {}
    context['image_form'] = ImageUploadForm()
    context['pk'] = pk
    context['current_user'] = request.user
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            user.profile_image = upload_result['url']
            user.save()
            return redirect('profilemanager:detail', slug=user.profile.slug)
        else:
            messages.error(request, "Invalid image.")

    return render(request, 'accounts/update_profile_picture.html', context=context)



def _send_confirmation_email(request, context, form):
    load_dotenv()
    user = form.save()
    print('send email')
    user.profile_image = 'https://res.cloudinary.com/dal73z4cj/image/upload/v1684772629/dinosaure_j44fyo.png'
    print('user profile image')
    user.save()
    email_confirmation = EmailConfirmation(user=user)
    email_confirmation.generate_token()
    email_confirmation.save()
    subject, message, from_email = _email_content(request, email_confirmation)
    send_mail(subject, message, from_email, [user.email])
    context['user'] = user

    return context


def _email_content(request, email_confirmation):
    subject = "Account activation"
    confirmation_url = request.build_absolute_uri(
        reverse('accounts:confirm_email', args=[email_confirmation.token]))
    message = f"Thank you for registering. Please click on the following link to confirm your account:\n\n{confirmation_url}"
    from_email = os.environ.get('EMAIL_HOST_USER')

    return subject, message, from_email
