import re
import urllib
import uuid
import jwt
from datetime import datetime, timedelta
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from users.decorators import  permissions_in_menu_required
from users.forms import AddressForm, EducationInfoForm, ExperienceForm, TrainingFormSet, ExperienceFormSet
from users.forms import RegisterForm, LoginForm, \
    BasicInfoUserForm, ProfileForm, AddressDetailsUserForm, TrainingForm, SocialMediaForm, EducationFormSet, \
    SocialFormSet, PasswordResetForm, UserRegisterFormByAdmin
from users.models import (AddressDetails, ExperienceDetails, Profile,
                          TrainingDetails, User, EducationDetails, SocialMedias)
from users.tasks import send_invitation_mail, send_mail_func, reset_mail_pass
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from users.utils import generate_confirmation_token, generate_password_token, generate_invitation_token
from django.core.paginator import Paginator
from roles.models import Role


class PersonalInfoView(View):
    template_name = 'users/personal_info.html'

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
            print("error")
        user_form = BasicInfoUserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        context = {"user_form": user_form, 'profile_form': profile_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = BasicInfoUserForm(request.POST, instance=request.user)

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
        if profile is not None:
            profile_form = ProfileForm(request.POST, instance=profile)
        else:
            profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            created_profile_form = profile_form.save(commit=False)
            created_profile_form.user = request.user
            created_profile_form.save()
            return redirect(reverse_lazy('users:address_info'))
        context = {"user_form": user_form, 'profile_form': profile_form}
        return render(request, self.template_name, context)


class AddressInfoView(FormView):
    template_name = 'users/address_info.html'

    def get(self, request, *args, **kwargs):
        try:
            address = AddressDetails.objects.get(user=request.user)
        except AddressDetails.DoesNotExist:
            address = None
        user_form = AddressDetailsUserForm(instance=request.user)
        address_form = AddressForm(instance=address)
        context = {"user_form": user_form, 'address_form': address_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = AddressDetailsUserForm(request.POST, instance=request.user)

        try:
            address = AddressDetails.objects.get(user=request.user)
        except AddressDetails.DoesNotExist:
            address = None
        if address is not None:
            address_form = AddressForm(request.POST, instance=address)
        else:
            address_form = AddressForm(request.POST)

        if address_form.is_valid():
            user_form.save()
            created_address_form = address_form.save(commit=False)
            created_address_form.user = request.user
            created_address_form.save()
            return redirect(reverse_lazy('users:education_info'))
        context = {"user_form": user_form, 'address_form': address_form}
        return render(request, self.template_name, context)


class EducationInfoView(View):
    template_name = 'users/education_info.html'
    form_class = EducationInfoForm

    def get(self, request, *args, **kwargs):
        formset = EducationFormSet(instance=request.user)
        if formset.total_form_count() == 0:
            formset.extra = 1
        context = {
            'formset': formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = EducationFormSet(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('users:training_info'))
        context = {
            'formset': formset
        }
        return render(request, self.template_name, context)


class TrainingInfoView(View):
    template_name = 'users/training_info.html'
    form_class = TrainingForm

    def get(self, request, *args, **kwargs):
        formset = TrainingFormSet(instance=request.user)
        if formset.total_form_count() == 0:
            formset.extra = 1
        context = {
            'formset': formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = TrainingFormSet(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('users:work_info'))
        context = {
            'formset': formset
        }
        return render(request, self.template_name, context)


class WorkInfoView(View):
    template_name = 'users/work_info.html'
    form_class = ExperienceForm

    def get(self, request, *args, **kwargs):
        formset = ExperienceFormSet(instance=request.user)
        if formset.total_form_count() == 0:
            formset.extra = 1
        context = {
            'formset': formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = ExperienceFormSet(request.POST, instance=request.user)
        context = {
            'formset': formset
        }
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('users:social_info'))
        return render(request, self.template_name, context)


class SocialInfoView(View):
    template_name = 'users/social_info.html'
    form_class = SocialMediaForm

    def get(self, request, *args, **kwargs):
        formset = SocialFormSet(instance=request.user)
        if formset.total_form_count() == 0:
            formset.extra = 1
        context = {
            'formset': formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = SocialFormSet(request.POST, instance=request.user)
        context = {
            'formset': formset
        }
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('users:social_info'))
        return render(request, self.template_name, context)


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
            last_name = form.cleaned_data['last_name']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            # unique username with the help of uuid 
            user.set_password(password1)

            preName = str(uuid.uuid4())
            preName = preName[:3]
            user.username = preName + first_name
            user.save()

            # for profile object
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            if user:
                profile = Profile.objects.create(user=user, date_of_birth=dob, gender=gender)
                profile.save()

            token_needed = generate_confirmation_token(user.pk)

            if not user.is_verified:
                status = send_mail_func.delay(
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

    return render(request, 'users/registration.html', context)


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
                return render(request, 'users/login.html', context)
            else:
                login(request, user)
                return redirect("pentest:home")

    return render(request, 'users/login.html', context)


@login_required
def logout_user(request):
    """
    Logout a user
    """
    logout(request)
    return redirect("users:login")


class RegistrationView(TemplateView):
    template_name = 'users/registration.html'


# def activate_user(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)

#     except Exception as e:
#         user = None

#     if user and account_activation_token.check_token(user, token):
#         user.is_verified = True
#         user.save()

#         messages.add_message(request, messages.SUCCESS,
#                              'Email verified, you can now login')
#         return redirect(reverse('users:login'))

#     return render(request, 'users/activate-failed.html')


def delete_single_form(request, str, pk):
    if str == 'education_info':
        Model = EducationDetails
    elif str == 'training_info':
        Model = TrainingDetails
    elif str == 'work_info':
        Model = ExperienceDetails
    elif str == 'social_info':
        Model = SocialMedias

    single_form = get_object_or_404(Model, id=pk)

    if request.method == 'POST':
        single_form.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


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
        return redirect('users:change-password')
    except jwt.DecodeError:
        messages.error(request, 'Error decoding confirmation token.')
        return redirect('users:change-password')
    except jwt.InvalidTokenError:
        messages.error(request, 'Invalid confirmation token.')
        return redirect('users:change-password')

    try:
        user = User.objects.get(pk=payload['confirm'])
        print(user)
    except User.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('users:change-password')

    if user.is_verified:
        messages.error(request, "Email already confirmed.")
    else:
        user.is_verified = True
        user.save()
        messages.success(request, "Email confirmed.")
    return redirect('users:login')



def passwordReset(request):
    user = request.user
    token = generate_password_token(user.pk)
    status = reset_mail_pass.delay(email=user.email, token=str(token))
    messages.success(request, 'A mail has been sent to your mailing address!')
    request.session['name'] = user.first_name
    return redirect('users:change-password')



def passwordConfirmFromEmail(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    except jwt.ExpiredSignature:
        messages.error(request, 'Confirmation token has expired.')
        return redirect('users:change-password')
    except jwt.DecodeError:
        messages.error(request, 'Error decoding confirmation token.')
        return redirect('users:change-password')
    except jwt.InvalidTokenError:
        messages.error(request, 'Invalid confirmation token.')
        return redirect('users:change-password')

    try:
        user = User.objects.get(pk=payload['confirm'])
    except User.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('users:change-password')

    messages.success(request, "You can change your password now.")
    return redirect('users:change-password')


def changePassword(request):
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
    return render(request, 'users/password_reset.html', context)



def resend_email(request):
    user = request.user
    token = generate_confirmation_token(user.pk)
    status = send_mail_func.delay(str(user), str(token))
    messages.success(request, 'A email has sent to your address. Please check!')
    return redirect('users:change-password')


# For User Management
@method_decorator(permissions_in_menu_required('User Management', ['can_view']), name='dispatch')
class UserListView(ListView):
    model = User
    # ordering = ["-date_joined"]
    context_object_name = "users"
    template_name = "users/list_users.html"
    paginate_by = 20


@method_decorator(permissions_in_menu_required('User Management', ['can_add']), name='dispatch')
class UserCreateView(View):
    template_name = "users/user-create.html"

    def get(self, request, *args, **kwargs):
        # try:
        #     user = User.objects.get(user=request.user)
        # except User.DoesNotExist:
        #     profile = None
        #     print("error")

        form = UserRegisterFormByAdmin()
        # profile_form = ProfileForm(instance=profile)
        context = {"form": form}
        context["roles"] = Role.objects.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pwd = User.objects.make_random_password(length=8)
        print(request.POST)
        updated_request = request.POST.copy()
        updated_request.update({"password": pwd})
        form = UserRegisterFormByAdmin(updated_request)
        print("before valid")
        if form.is_valid():
            print("after valid")
            user = form.save(commit=False)
            user.set_password(pwd)
            user.save()
            token = generate_invitation_token(form.instance.id)
            send_invitation_mail.delay(email=form.instance.email, token=str(token), pwd=pwd)
            return redirect(reverse_lazy('users:list_user'))
        print("outside valid")
        print(form.errors)
        context = {
            'form': form,
            "roles": Role.objects.all()
        }
        return render(request, self.template_name, context)


# def userCreateView(request):
#     form = RegisterForm(data=request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#         pwd = User.objects.create_random_password(length=)make_random_password(length=8)
#         email = form.cleaned_data['email']

# class UserUpdateView(UpdateView):
#     model = User
#     template_name = "users/user-update.html"
#     fields = ["first_name", "middle_name", "last_name", "roles"]
#     # form_class = UserRegisterFormByAdmin
#     # fields = ['first_name', "middle_name", "last_name",'username', 'email', 'password','roles']
#     success_url = reverse_lazy('users:list_user')

#     def get_context_data(self, **kwargs):
#         # print(self.kwargs['pk'])
#         context = super().get_context_data(**kwargs)
#         context["roles"] =  Role.objects.all()
#         # context["own_role"] = Role.objects.filter(users=self.request.user)
#         # context['own_role'] = 
#         # form = context['form']
#         # form.initial = {"first_name": 'jpt',"roles": Role.objects.filter(users=self.request.user)}
#         # print(form.initial)
#         # # print(form)
#         # context['form']=form
#         # print(form)
#         # context['']
#         return context

@method_decorator(permissions_in_menu_required('User Management', ['can_change']), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = "users/user-update.html"
    fields = ["first_name", "middle_name", "last_name", "username", "roles"]
    success_url = reverse_lazy("users:list_user")
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Role.objects.all()
        return context


# class UserDeleteView(DeleteView):
#     model = User
#     template_name = "users/list_users.html"
#     success_url = reverse_lazy('users:list_user')

@permissions_in_menu_required('User Management', ['can_delete'])
def userDeleteView(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.success(request, "A user has been deleted.")
    return redirect('users:list_user')


@permissions_in_menu_required('User Management', ['can_delete'])
def user_deactivate(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        user.is_active = False
        user.save()
        messages.success(request, " User account has been successfully deactivated! ")
        return redirect("users:list_user")


@permissions_in_menu_required('User Management', ['can_delete'])
def user_activate(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        user.is_active = True
        user.save()
        messages.success(request, " User account has been successfully activated! ")
        return redirect("users:list_user")
