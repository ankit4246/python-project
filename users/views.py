from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from users.forms import BasicInformation, AddressInfo, EducationInfo
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

class TrainingInfoView(TemplateView):
    template_name = 'users/training_info.html'


class WorkInfoView(TemplateView):
    template_name = 'users/work_info.html'


class SocialInfoView(TemplateView):
    template_name = 'users/social_info.html'



