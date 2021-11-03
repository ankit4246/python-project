from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from users.forms import BasicInformation, AddressInfo, EducationInfo, ExperienceForm, RegisterForm, LoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from users.models import User
from django.contrib.auth.decorators import login_required
import uuid

class PersonalInfoView(FormView):
    template_name = 'users/personal_info.html'
    form_class = BasicInformation
    success_url = reverse_lazy('address_info')


class AddressInfoView(FormView):
    template_name = 'users/address_info.html'
    form_class = AddressInfo
    success_url = reverse_lazy('education_info')


class EducationInfoView(FormView):
    template_name = 'users/education_info.html'
    form_class = EducationInfo
    success_url = reverse_lazy('training_info')


class TrainingInfoView(FormView):
    template_name = 'users/training_info.html'
    form_class = EducationInfo
    success_url = reverse_lazy('work_info')


class WorkInfoView(FormView):
    template_name = 'users/work_info.html'
    form_class = ExperienceForm
    success_url = reverse_lazy('social_info')


class SocialInfoView(FormView):
    template_name = 'users/social_info.html'
    form_class = ExperienceForm
    success_url = reverse_lazy('social_info')


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
            # unique username with the help of uuid 
            user.password = password1
            preName = str(uuid.uuid4())
            preName = preName[:3]
            user.username = preName + first_name
            user.save()
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