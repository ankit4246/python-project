from django import forms
from django.forms import inlineformset_factory
from users.models import Profile, TrainingDetails, ExperienceDetails, SocialMedias, User
from users.models import Profile, AddressDetails, EducationDetails
from django import forms
from django.contrib.auth import password_validation
import re
from django.contrib.admin import widgets
from users.tasks import send_mail_func


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


MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married')]


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


DURATION_TYPE_CHOICES = [('Month', 'Month'), ('Year', 'Year')]


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
        widgets = {
            'duration': forms.widgets.TextInput(attrs={'id': 'marksSecuredNum'}),
            'duration_type': forms.widgets.Select(choices=DURATION_TYPE_CHOICES,
                                                  attrs={'id': 'marksSecured'}),
            'completion_month': forms.widgets.SelectDateWidget(
                attrs={'id': 'marksSecured', 'type': 'month'}),
            'completion_year': forms.widgets.SelectDateWidget(
                attrs={'id': 'marksSecured', 'type': 'year'}),
        }


JOB_LEVEL_CHOICES = [('Intern', 'Intern'),
                     ('Junior', 'Junior'),
                     ('Mid', 'Mid'),
                     ('Senior', 'Senior'),
                     ]


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceDetails
        fields = (
            'institute_name',
            'location',
            'designation',
            'job_level',
            'start_date',
            'is_current',
            'jd',
            'user',
        )
        widgets = {
            'jd': forms.widgets.Textarea(),
            'job_level': forms.widgets.Select(choices=JOB_LEVEL_CHOICES,
                                              attrs={'class': 'marital'}),
        }


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedias
        fields = (
            'social_media',
            'link',
        )


LOCAL_BODY_CHOICES = [('Local Body 1', 'Local Body 1'), ('Local Body 2', 'Local Body 2')]


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


GPA_TYPE_CHOICES = [('Percentage', 'Percentage'),
                    ('GPA', 'GPA')]
EDU_LEVEL_CHOICES = [('Bachelors', 'Bachelors'),
                     ('Masters', 'Masters')]


# class EducationInfoForm(forms.ModelForm):
#     graduation_year = forms.IntegerField()
#     graduation_month = forms.IntegerField()
#
#     class Meta:
#         model = EducationDetails
#         fields = (
#             'university',
#             'edu_level',
#             'faculty',
#             'per_gpa_type',
#             'per_gpa_value',
#             'passed_date',
#             'user',
#             'graduation_year',
#             'graduation_month',
#         )
#         widgets = {
#             'edu_level': forms.widgets.Select(choices=EDU_LEVEL_CHOICES,
#                                               attrs={'class': 'maritalStatus'}),
#             'faculty': forms.widgets.TextInput(attrs={'class': 'personalDetail-fname'}),
#             'university': forms.widgets.Select(attrs={'class': 'maritalStatus'}),
#             'graduation_year':forms.widgets.SelectDateWidget(attrs={'class': 'maritalStatus'}),
#             'graduation_month':forms.widgets.SelectDateWidget(attrs={'class': 'maritalStatus'}),
#             # 'passed_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'maritalStatus'}),
#             'per_gpa_type': forms.widgets.Select(choices=GPA_TYPE_CHOICES,
#                                                  attrs={'id': 'marksSecured'}),
#             'per_gpa_value': forms.widgets.TextInput(attrs={'id': 'marksSecuredNum'})
#         }


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
            'passed_date',
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
            'per_gpa_value': forms.widgets.TextInput(attrs={'id': 'marksSecuredNum'})
        }


EducationFormSet = inlineformset_factory(User, EducationDetails,
                                         fields='__all__',
                                         form=EducationInfoForm,
                                         extra=0,
                                         )


# class RegistrationForm(ModelForm):
#     CHOICES = (
#         ("male", "male"),
#         ("female", "female"),
#         ("others", "others"),
#     )
#     password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'size':20}))
#     password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'size':20}))
#     dob = forms.DateTimeField()
#     gender = forms.ChoiceField(choices=CHOICES)
#     class Meta:
#         model = User
#         fields = ['first_name', "middle_name", 'last_name', 'email', 'password1', 'password2', 'dob', 'gender']


class LoginForm(forms.Form):
    """
    Form to login a user
    """
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your  email'}),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            user = None

        if user:
            return user.email
        return None


class RegisterForm(forms.ModelForm):
    """
    Form to register a new user
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password again'}),
        strip=False,
    )

    CHOICES = (
        ("male", "male"),
        ("female", "female"),
        ("others", "others"),
    )

    dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'dob',
            'gender',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your middle name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password1']
        confirm_password = self.cleaned_data['password2']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        if first_name.lower() in password.lower() or last_name.lower() in password.lower():
            raise forms.ValidationError('Password similar to name of user.')
        password_validation.validate_password(confirm_password, self.instance)
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            raise forms.ValidationError('Invalid Email format')
        return email

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     # user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     print("user",user)
    #     # email_celery = json.dumps(user)
    #     # send_mail_func.delay(instance=User.objects.filter(pk=user.pk).values('email'))
    #     return user