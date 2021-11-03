from django import forms
import json
from users.models import Profile, TrainingDetails, ExperienceDetails, SocialMedias, User
from users.models import Profile, AddressDetails, EducationDetails
from django import forms
from django.contrib.auth import password_validation
import re
from django.contrib.admin import widgets
from users.tasks import send_mail_func


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
        print("clean")
        try:
            user = User.objects.get(email=username)
            print("email", User.objects.get(email=username))
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

    dob = forms.DateField(widget=widgets.AdminDateWidget)
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