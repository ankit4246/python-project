import uuid

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from users.forms import AddressForm, EducationInfoForm, ExperienceForm, TrainingFormSet, ExperienceFormSet
from users.forms import RegisterForm, LoginForm, \
    BasicInfoUserForm, ProfileForm, AddressDetailsUserForm, TrainingForm, SocialMediaForm, EducationFormSet, \
    SocialFormSet
from users.models import (AddressDetails, ExperienceDetails, Profile,
                          TrainingDetails, User)
from users.tasks import send_mail_func
from .tokens import account_activation_token


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
        for form in formset:
            print(form.errors)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('users:training_info'))
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
        context = {
            'formset': formset
        }
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('users:work_info'))
        return render(request, self.template_name, context)


# class TrainingInfoView(View):
#     template_name = 'users/training_info.html'
#     form_class = TrainingForm
#
#     def get(self, request, *args, **kwargs):
#         formset = self.TrainingFormSet(instance=request.user)
#         context = {
#             'formset': formset
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST or None)
#         context = {
#             'form': form
#         }
#         if form.is_valid():
#             created_training = form.save(commit=False)
#             created_training.user = request.user
#             created_training.save()
#             return redirect(reverse_lazy('users:work_info'))
#         return render(request, self.template_name, context)
#

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


# class RegistrationView(TemplateView):
#     template_name = 'users/registration.html'

# def register(request):
#     if request.method == "POST":
#         fm = RegistrationForm(request.POST)
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 != password2:
#             raise ValidationError("password must match")

#         if fm.is_valid():
#             user = fm.save(commit=False)
#             first_name = fm.cleaned_data['first_name']
#             last_name = fm.cleaned_data['last_name']
#             password1 = fm.cleaned_data['password1']
#             user.password = password1
#             user.username = first_name + ' ' + last_name
#             user.save()
#             RegistrationForm()
#             return redirect(reverse("login"))
#     else:
#         fm = RegistrationForm()
#         return render(request, 'users/registration.html', {'form':fm,})

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

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            print("current-domain", current_site)
            print('current_uid', uid)
            print('current_token', token)

            if not user.is_verified:
                send_mail_func.delay(
                    # email, uid=uid, token=token
                    email=email, current_site=current_site, uid=uid, token=token
                    # user_id=user.pk
                    # current_site=current_site,
                    # uid=uid,
                    # token=token
                )
                messages.success(request, "Check your email!")
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
                return redirect("users:personal_info")

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


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('users:login'))

    return render(request, 'users/activate-failed.html')
