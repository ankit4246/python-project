from django import forms

from users.models import Profile, TrainingDetails, ExperienceDetails, SocialMedias
from users.models import Profile, AddressDetails, EducationDetails


class BasicInformationForm(forms.ModelForm):
    first_name = forms.CharField(max_length='100')
    middle_name = forms.CharField(max_length='100')
    last_name = forms.CharField(max_length='100')

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'father_full_name',
            'mother_full_name',
            'spouse_full_name',
            'marital_status',
            'nationality',
            'date_of_birth',
            'pan_number',
            'national_identity_num',
            'gender',
            'user',
        )


class TrainingForm(forms.ModelForm):
    class Meta:
        model = TrainingDetails
        fields = (
            'name_of_training',
            'institute_name',
            'duration',
            'duration_type',
            'completion_month',
            'completion_year',
            'user',
        )


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceDetails
        fields = (
            'institute_name',
            'designation',
            'job_level',
            'start_date',
            'jd',
            'user',
        )


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedias
        fields = (
            'social_media',
            'link',
            'user',
        )


class AddressInfo(forms.ModelForm):
    mobile_no = forms.CharField(max_length=10)

    class Meta:
        model = AddressDetails
        fields = (
            'address',
            'province',
            'country',
            'district',
            'ward_no',
            'tole',
            'house_no',
            'user',
            'mobile_no',
        )


class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        fields = (
            'university',
            'edu_level',
            'faculty',
            'per_gpa_type',
            'per_gpa_value',
            'passed_date',
            'user',
        )
