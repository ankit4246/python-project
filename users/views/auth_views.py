import uuid
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from users.forms.auth_forms import RegisterForm, LoginForm, \
    PasswordResetForm
from users.models import (Profile,
                          User)
from users.tasks import send_mail_func, reset_mail_pass
from users.utils import generate_confirmation_token, generate_password_token


def user_register(request):
    """
    Register a user
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            # unique username with the help of uuid
            user.set_password(password1)
            pre_name = str(uuid.uuid4())
            pre_name = pre_name[:3]
            user.username = pre_name + first_name
            user.save()

            # for profile object
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            if user:
                profile = Profile.objects.create(user=user, date_of_birth=dob, gender=gender)
                profile.save()

            token_needed = generate_confirmation_token(user.pk)

            if not user.is_verified:
                send_mail_func.delay(
                    # email=email, current_site=str(current_site), uid=uid, token=token_needed
                    email=email, token=str(token_needed)
                )
                messages.success(request, "Check your email!")
                messages.add_message(request, messages.INFO, 'Hello world.')
            # request.session['current_site'] = str(current_site)
            request.session['token'] = str(token_needed)
            request.session['name'] = first_name
            return redirect("users:login")

    context = {
        'form': form
    }

    return render(request, 'users/auth/registration.html', context)


def login_user(request):
    """
    Login a user
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm(data=request.POST or None)
    context = {
        'form': form,
    }

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(email=username, password=password)

            print("user", user)
            if user is None:
                messages.error(request, "Invalid login credentials")
                return render(request, 'users/auth/login.html', context)
            else:
                login(request, user)
                return redirect("pentest:home")

    return render(request, 'users/auth/login.html', context)


@login_required
def logout_user(request):
    """
    Logout a user
    """
    logout(request)
    return redirect("users:login")


class RegistrationView(TemplateView):
    template_name = 'users/auth/registration.html'


def user_confirm_email(request, token):
    # if request.user.is_authenticated:
    #     return redirect('/')

    # token = request.GET.get('token')
    if token is None:
        raise Http404()
    print("Output_token", token)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    except jwt.ExpiredSignature:
        messages.error(request, 'Confirmation token has expired.')
        return redirect('users:change_password')
    except jwt.DecodeError:
        messages.error(request, 'Error decoding confirmation token.')
        return redirect('users:change_password')
    except jwt.InvalidTokenError:
        messages.error(request, 'Invalid confirmation token.')
        return redirect('users:change_password')

    try:
        user = User.objects.get(pk=payload['confirm'])
        print(user)
    except User.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('users:change_password')

    if user.is_verified:
        messages.error(request, "Email already confirmed.")
    else:
        user.is_verified = True
        user.save()
        messages.success(request, "Email confirmed.")
    return redirect('users:login')


def password_reset(request):
    user = request.user
    token = generate_password_token(user.pk)
    status = reset_mail_pass.delay(email=user.email, token=str(token))
    messages.success(request, 'A mail has been sent to your mailing address!')
    request.session['name'] = user.first_name
    return redirect('users:change_password')


def password_confirm_from_email(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    except jwt.ExpiredSignature:
        messages.error(request, 'Confirmation token has expired.')
        return redirect('users:change_password')
    except jwt.DecodeError:
        messages.error(request, 'Error decoding confirmation token.')
        return redirect('users:change_password')
    except jwt.InvalidTokenError:
        messages.error(request, 'Invalid confirmation token.')
        return redirect('users:change_password')

    try:
        User.objects.get(pk=payload['confirm'])
    except User.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('users:change_password')

    messages.success(request, "You can change your password now.")
    return redirect('users:change_password')


def change_password(request):
    form = PasswordResetForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has successfully changed")
            return redirect('users:login')
    else:
        form = PasswordResetForm()
    context = {
        "form": form,
    }
    return render(request, 'users/auth/password_reset.html', context)


def resend_email(request):
    user = request.user
    token = generate_confirmation_token(user.pk)
    status = send_mail_func.delay(str(user), str(token))
    messages.success(request, 'A email has sent to your address. Please check!')
    return redirect('users:change_password')
