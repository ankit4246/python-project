from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from users.forms import BasicInformation, AddressInfo, EducationInfo, ExperienceForm
from django.urls import reverse_lazy


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


class RegistrationView(TemplateView):
    template_name = 'users/registration.html'

