import os

import cloudinary
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from dotenv import load_dotenv

from accounts.forms import CustomSignupForm, ImageUploadForm, CustomUpdateForm
from accounts.models import EmailConfirmation, CustomUser
from profilemanager.models import Company


def signup(request):
    context = {}
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # Gérer si le user,category est dev ou client, puis modifier le mail de confirmation en fonction
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
        print(user)
        if user.category == 'company':
            user.company = _create_company_profile(user)
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


def update_profile_picture(request, slug, pk):
    context = {}
    context['image_form'] = ImageUploadForm()
    context['slug'] = slug
    context['pk'] = pk
    context['current_user'] = request.user
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        user = get_object_or_404(CustomUser, pk=pk)
        if form.is_valid():
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            user.profile_image = upload_result['url']
            user.save()
            return redirect('profilemanager:detail', slug=slug, pk=pk)
        else:
            messages.error(request, "Invalid image.")

    return render(request, 'accounts/update_profile_picture.html', context=context)


@login_required
def update_profile_info(request, slug, pk):
    if request.user.pk != pk:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation d'effectuer cette action.")

    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUpdateForm(request.POST, instance=user)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            if request.headers.get('HX-Request'):
                html = render_to_string('accounts/partials/phone_number_partial.html', {'phone_number': user.phone_number})
                return HttpResponse(html)
            return redirect('profilemanager:detail', slug=slug, pk=pk)
        else:
            if request.headers.get('HX-Request'):
                errors_html = render_to_string('accounts/partials/errors.html', {'user': user, 'profile_form': form})
                return HttpResponse(errors_html)
            return redirect('profilemanager:detail', slug=slug, pk=pk)

    return redirect('profilemanager:detail', slug=slug, pk=pk)


def update_phone_display(request, pk):
    pass


def _send_confirmation_email(request, context, form):
    load_dotenv()
    user = form.save()
    user.profile_image = 'https://res.cloudinary.com/dal73z4cj/image/upload/v1684772629/dinosaure_j44fyo.png'
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

def _create_company_profile(user):
    user_company = Company.objects.create(user=user)
    return user_company
