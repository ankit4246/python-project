from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from users.forms.kyc_forms import AddressForm, EducationInfoForm, ExperienceForm, TrainingFormSet, ExperienceFormSet
from users.forms.kyc_forms import BasicInfoUserForm, ProfileForm, AddressDetailsUserForm, TrainingForm, SocialMediaForm, \
    EducationFormSet, \
    SocialFormSet
from users.models import (AddressDetails, ExperienceDetails, Profile,
                          TrainingDetails, EducationDetails, SocialMedias)


class PersonalInfoView(View):
    template_name = 'users/kyc/personal_info.html'

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


class AddressInfoView(View):
    template_name = 'users/kyc/address_info.html'

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
    template_name = 'users/kyc/education_info.html'
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
    template_name = 'users/kyc/training_info.html'
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
    template_name = 'users/kyc/work_info.html'
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
    template_name = 'users/kyc/social_info.html'
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


def delete_single_form(request, str, pk):
    if str == 'education_info':
        model = EducationDetails
    elif str == 'training_info':
        model = TrainingDetails
    elif str == 'work_info':
        model = ExperienceDetails
    elif str == 'social_info':
        model = SocialMedias

    single_form = get_object_or_404(model, id=pk)

    if request.method == 'POST':
        single_form.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )
