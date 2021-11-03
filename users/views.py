from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from users.forms import BasicInformationForm, AddressInfo, EducationInfoForm, ExperienceForm
from django.urls import reverse_lazy

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


class RegistrationView(TemplateView):
    template_name = 'users/registration.html'
