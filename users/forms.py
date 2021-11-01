from django.forms import ModelForm

from users.models import LoginCred, Profile, TrainingDetails, ExperienceDetails, SocialMedias, User
from users.models import Profile, AddressDetails, EducationDetails
from django import forms

class BasicInformation(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class TrainingForm(ModelForm):
    class Meta:
        model = TrainingDetails
        fields = '__all__'


class ExperienceForm(ModelForm):
    class Meta:
        model = ExperienceDetails
        fields = '__all__'


class SocialMediaForm(ModelForm):
    class Meta:
        model = SocialMedias
        fields = '__all__'


class AddressInfo(ModelForm):
    class Meta:
        model = AddressDetails
        fields = '__all__'


class EducationInfo(ModelForm):
    class Meta:
        model = EducationDetails
        fields = '__all__'

class RegistrationForm(ModelForm):
    CHOICES = (
        ("male", "male"),
        ("female", "female"),
        ("others", "others"),
    )
    password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'size':20}))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'size':20}))
    dob = forms.DateTimeField()
    gender = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = User
        fields = ['first_name', "middle_name", 'last_name', 'email', 'password1', 'password2', 'dob', 'gender']

class LoginCredForm(ModelForm):
    class Meta:
        model = LoginCred
        fields = '__all__'