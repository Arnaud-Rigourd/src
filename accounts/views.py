import os

import cloudinary
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, EmailMultiAlternatives
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
        if user.category == 'company':
            user.company = _create_company_profile(user)
        elif user.category == 'developpeur':
            subject, text_message, html_message, from_email = _introduction_email_content(user)
            email = EmailMultiAlternatives(subject, text_message, from_email, [user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()
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

    subject, message, from_email = _confirmation_email_content(request, email_confirmation)
    send_mail(subject, message, from_email, [email])
    messages.success(request, "Email sent successfully. Please check your inbox.")
    return render(request, 'registration/email_confirmation_done.html', context={'user': user})


def signin(request):
    """Handles the sign-in process for a user.

    This view function handles both GET and POST requests. On a GET request, it renders
    the login form. On a POST request, it validates the form and logs in the user.

    If the user is logging in for the first time and their category is 'developpeur',
    they are redirected to the profile creation page. Otherwise, they are redirected
    to the home page.

    If the form is not valid (i.e., the username or password is incorrect),
    an error message is generated.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object. On a GET request or if the form is invalid,
            this is a rendered login form. On a successful POST request, this is a
            redirect to either the profile creation page or the home page.
    """
    # Handle form for GET request
    if request.method != 'POST':
        return render(request, "registration/login.html", context={'form': AuthenticationForm()})

    form = AuthenticationForm(data=request.POST)

    # Handle invalid form
    if not form.is_valid():
        messages.error(request, "Invalid username or password.")
        return render(request, "registration/login.html", context={'form': form})

    user = form.get_user()

    # Redirect new 'developpeur' user to profile creation page
    if user.category == 'developpeur' and user.last_login is None:
        login(request, user)
        return redirect('profilemanager:create', username=request.user.username)
    login(request, user)
    return redirect('interfacemanager:home')


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


def _send_confirmation_email(request, context, form: CustomSignupForm) -> 'context':
    load_dotenv()
    user = _setup_default_profile_image(form)
    email_confirmation = EmailConfirmation(user=user)
    email_confirmation.generate_token()
    email_confirmation.save()
    subject, message, from_email = _confirmation_email_content(request, email_confirmation)
    send_mail(subject, message, from_email, [user.email])
    context['user'] = user

    return context


def _confirmation_email_content(request, email_confirmation):
    subject = "Activation de votre compte DevForFree"
    confirmation_url = request.build_absolute_uri(
        reverse('accounts:confirm_email', args=[email_confirmation.token]))
    message = f"Merci de vous être enregistré. Afin de finaliser votre inscription, veuillez cliquer sur le lien suivant pour confirmer votre adresse mail : \n\n{confirmation_url}"
    from_email = os.environ.get('EMAIL_HOST_USER')

    return subject, message, from_email


def _introduction_email_content(user: CustomUser):
    subject = "Bienvenue sur DevForFree ! 👩‍💻🧑‍💻"
    text_message = render_to_string('accounts/partials/text_introduction_dev_email.html', {'user': user})
    html_message = render_to_string('accounts/partials/html_introduction_dev_email.html', {'user': user})
    from_email = os.environ.get('EMAIL_HOST_USER')
    return subject, text_message, html_message, from_email


def _setup_default_profile_image(form: CustomSignupForm) -> CustomUser:
    user = form.save()
    user.profile_image = 'https://res.cloudinary.com/dal73z4cj/image/upload/v1684772629/dinosaure_j44fyo.png'
    user.save()

    return user


def _create_company_profile(user: CustomUser) -> CustomUser:
    user_company = Company.objects.create(user=user)
    return user_company
