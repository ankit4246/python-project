import re
from django import forms
from django.forms import inlineformset_factory
from users.models import Profile, AddressDetails, EducationDetails
from users.models import TrainingDetails, ExperienceDetails, SocialMedias, User, MONTH_CHOICES, YEAR_CHOICES

GPA_TYPE_CHOICES = [('Percentage', 'Percentage'),
                    ('GPA', 'GPA')]
EDU_LEVEL_CHOICES = [('Bachelors', 'Bachelors'),
                     ('Masters', 'Masters')]
MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married')]
DURATION_TYPE_CHOICES = [('Month', 'Month'), ('Year', 'Year')]
JOB_LEVEL_CHOICES = [('Intern', 'Intern'),
                     ('Junior', 'Junior'),
                     ('Mid', 'Mid'),
                     ('Senior', 'Senior'),
                     ]
LOCAL_BODY_CHOICES = [('Local Body 1', 'Local Body 1'), ('Local Body 2', 'Local Body 2')]


class BasicInfoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'first_name',
            'middle_name',
            'last_name',
        }


class AddressDetailsUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'email',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {
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
        }
        widgets = {
            'date_of_birth': forms.widgets.DateInput(attrs={'type': 'date'}),
            'marital_status': forms.widgets.Select(choices=MARITAL_STATUS_CHOICES,
                                                   attrs={'id': 'marital'}),
            'gender': forms.widgets.Select(attrs={'id': 'marital'}),
        }


class TrainingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fields['name_of_training'].required = True
        self.fields['institute_name'].required = True
        self.fields['duration'].required = True


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
        widgets = {
            'duration': forms.widgets.TextInput(attrs={'id': 'marksSecuredNum'}),
            'duration_type': forms.widgets.Select(choices=DURATION_TYPE_CHOICES,
                                                  attrs={'id': 'marksSecured'}),
            'completion_month': forms.widgets.Select(choices=MONTH_CHOICES,
                                                     attrs={'id': 'marksSecured'}),
            'completion_year': forms.widgets.Select(choices=YEAR_CHOICES,
                                                    attrs={'id': 'marksSecured'}),
        }

    def clean(self):

        # data from the form is fetched using super function
        super(TrainingForm, self).clean()

        # extract the username and text field from the data
        name_of_training = self.cleaned_data.get('name_of_training')
        institute_name = self.cleaned_data.get('institute_name')
        duration = self.cleaned_data.get('duration')

        # text = self.cleaned_data.get('text')

        if not re.match(r"[A-Za-z]{2,25}( [A-Za-z]{2,25})?", name_of_training):
            self._errors['name_of_training'] = self.error_class([
                'Invalid Name of Training'])

        if not re.match(r"[a-zA-Z]{3,30}", institute_name):
            self._errors['institute_name'] = self.error_class([
                'Invalid Name of Institute Name'])

        # if int(duration):
        #     self._errors['duration'] = self.error_class([
        #         'Invalid Duration'])
        # raise forms.ValidationError('Invalid Name of Training')

        # return any errors if found
        return self.cleaned_data


TrainingFormSet = inlineformset_factory(User, TrainingDetails,
                                        form=TrainingForm,
                                        extra=0,
                                        )


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceDetails
        fields = (
            'institute_name',
            'location',
            'designation',
            'job_level',
            'start_month',
            'start_year',
            'is_current',
            'jd',
            'user',
        )
        widgets = {
            'jd': forms.widgets.Textarea(),
            'job_level': forms.widgets.Select(choices=JOB_LEVEL_CHOICES,
                                              attrs={'id': 'marksSecured'}),
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'start_month': forms.widgets.Select(choices=MONTH_CHOICES,
                                                attrs={'id': 'marksSecured'}),
            'start_year': forms.widgets.Select(choices=YEAR_CHOICES,
                                               attrs={'id': 'marksSecured'}),
            'is_current': forms.widgets.CheckboxInput()
        }


ExperienceFormSet = inlineformset_factory(User, ExperienceDetails,
                                          form=ExperienceForm,
                                          extra=0,
                                          )


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedias
        fields = (
            'social_media',
            'link',
        )


SocialFormSet = inlineformset_factory(User, SocialMedias,
                                      form=SocialMediaForm,
                                      extra=0,
                                      )


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressDetails
        fields = (
            'address',
            'province',
            'country',
            'local_body',
            'district',
            'ward_no',
            'tole',
            'house_no',
            'user',
            'mobile_no',
        )
        widgets = {
            'local_body': forms.widgets.Select(choices=LOCAL_BODY_CHOICES,
                                               attrs={'id': 'marital'}),
            'address': forms.Textarea(),
            'country': forms.widgets.Select(attrs={'id': 'marital'}),
            'province': forms.widgets.Select(attrs={'id': 'marital'}),
            'district': forms.widgets.Select(attrs={'id': 'marital'}),
        }


class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        fields = (
            'university',
            'edu_level',
            'faculty',
            'institution_name',
            'per_gpa_type',
            'per_gpa_value',
            'passed_month',
            'passed_year',
            'user',
        )
        widgets = {
            'edu_level': forms.widgets.Select(choices=EDU_LEVEL_CHOICES,
                                              attrs={'id': 'marital'}),
            'faculty': forms.widgets.TextInput(attrs={'class': 'personalDetail-fname'}),
            'university': forms.widgets.Select(attrs={'id': 'marital'}),
            'passed_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'maritalStatus'}),
            'per_gpa_type': forms.widgets.Select(choices=GPA_TYPE_CHOICES,
                                                 attrs={'id': 'marksSecured'}),
            'per_gpa_value': forms.widgets.TextInput(attrs={'id': 'marksSecuredNum'}),
            'passed_month': forms.widgets.Select(choices=MONTH_CHOICES,
                                                 attrs={'id': 'marksSecured'}),
            'passed_year': forms.widgets.Select(choices=YEAR_CHOICES,
                                                attrs={'id': 'marksSecured'}),
        }


EducationFormSet = inlineformset_factory(User, EducationDetails,
                                         fields='__all__',
                                         form=EducationInfoForm,
                                         extra=0,
                                         )
