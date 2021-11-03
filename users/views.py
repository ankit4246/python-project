from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from users.forms import BasicInformationForm, AddressInfo, EducationInfoForm, ExperienceForm, RegisterForm, LoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from users.models import User
from django.contrib.auth.decorators import login_required
import uuid
from django.views.generic.edit import FormView, CreateView
from users.forms import BasicInformationForm, AddressInfo, EducationInfoForm, ExperienceForm
from django.urls import reverse_lazy
from users.tasks import send_mail_func
import json
# class PersonalInfoView(View):
#     template_name = 'users/personal_info.html'
#     form_class = BasicInformationForm
#     success_url = reverse_lazy('users:address_info')
from users.models import User, Profile, EducationDetails, TrainingDetails, ExperienceDetails, SocialMedias


class PersonalInfoView(View):
    template_name = 'users/personal_info.html'
    form_class = BasicInformationForm

    def get(self, request, *args, **kwargs):
        # get first, middle, last name from user model and return it
        # profile = Profile.objects.get(user=request.user)
        context = {"form": self.form_class(), 'user': request.user, 'profile': 'profile'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # extract first middle and last name from the form
            first_name = form.cleaned_data.pop('first_name')
            middle_name = form.cleaned_data.pop('middle_name')
            last_name = form.cleaned_data.pop('last_name')

            # add authenticated user to the 'user' field of cleaned data
            # form.cleaned_data['user'] = request.user
            # update authenticated user with first, middle and last name
            User.objects.filter(pk=request.user.pk).update(first_name=first_name, middle_name=middle_name,
                                                           last_name=last_name)
            # save the form
            form.save(commit=True)
        return redirect(reverse_lazy('users:address_info'))


class AddressInfoView(FormView):
    template_name = 'users/address_info.html'
    form_class = AddressInfo


class EducationInfoView(View):
    template_name = 'users/education_info.html'
    form_class = EducationInfoForm
    success_url = reverse_lazy('users:training_info')

    def get(self, request, *args, **kwargs):
        # education = EducationDetails.objects.get(user=request.user)
        context = {"form": self.form_class(), 'user': request.user, 'education': 'education'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return redirect(reverse_lazy('users:training_info'))


class TrainingInfoView(View):
    template_name = 'users/training_info.html'
    form_class = EducationInfoForm

    def get(self, request, *args, **kwargs):
        # training = TrainingDetails.objects.get(user=request.user)
        context = {"form": self.form_class(), 'user': request.user, 'training': 'training'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return redirect(reverse_lazy('users:work_info'))


class WorkInfoView(View):
    template_name = 'users/work_info.html'
    form_class = ExperienceForm

    def get(self, request, *args, **kwargs):
        # experience = ExperienceDetails.objects.get(user=request.user)
        context = {"form": self.form_class(), 'user': request.user, 'experience': 'experience'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return redirect(reverse_lazy('users:social_info'))


class SocialInfoView(View):
    template_name = 'users/social_info.html'
    form_class = ExperienceForm

    def get(self, request, *args, **kwargs):
        # social_media = SocialMedias.objects.get(user=request.user)
        context = {"form": self.form_class(), 'user': request.user, 'social_media': 'social_media'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return redirect(reverse_lazy('users:social_info'))


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
            user.password = password1
            preName = str(uuid.uuid4())
            preName = preName[:3]
            user.username = preName + first_name
            user.save()
            send_mail_func.delay(
                user_id=user.pk
            )
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
            user = User.objects.get(email=username, password=password)
            print("user", user)
            if user is None:
                # messages.error(request, "Invalid login credentials")
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
