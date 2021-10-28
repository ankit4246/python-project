from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from users.models import Profile


class PersonalInfoView(TemplateView):
    template_name = 'users/personal_info.html'


class AddressInfoView(TemplateView):
    template_name = 'users/address_info.html'


class EducationInfoView(TemplateView):
    template_name = 'users/education_info.html'


class TrainingInfoView(TemplateView):
    template_name = 'users/training_info.html'


class WorkInfoView(TemplateView):
    template_name = 'users/work_info.html'


class SocialInfoView(TemplateView):
    template_name = 'users/social_info.html'



