from django import forms
from django.forms import inlineformset_factory
from users.models import Profile, TrainingDetails, ExperienceDetails, SocialMedias, User, MONTH_CHOICES, YEAR_CHOICES
from users.models import Profile, AddressDetails, EducationDetails
from django import forms
from django.contrib.auth import get_user_model, password_validation
import re
from django.contrib.admin import widgets


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

        if not re.match(r"[a-zA-Z]{3,30}", name_of_training):
            self._errors['name_of_training'] = self.error_class([
                'Invalid Name of Training'])

        if not re.match(r"[a-zA-Z]{3,30}", name_of_training):
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
        ("M", "male"),
        ("F", "female"),
        ("O", "others"),
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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password1')
    #     confirm_password = cleaned_data.get('password2')
    #     first_name = cleaned_data.get('first_name')
    #     middle_name = cleaned_data.get('middle_name')
    #     last_name = cleaned_data.get('last_name')
    #     email = cleaned_data.get("email")
        
        # if not re.match(r"[a-zA-Z]{3,30}", first_name):
        #     raise forms.ValidationError('Invalid First Name')
        # if not re.match(r"[a-zA-Z]{3,30}", middle_name):
        #     raise forms.ValidationError('Invalid Middle Name')
        # if not re.match(r"[a-zA-Z]{3,30}", last_name):
        #     raise forms.ValidationError('Invalid Last Name')
        # if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        #     raise forms.ValidationError('Invalid Email format')
        # if len(password) < 8 and len(confirm_password) < 8:
        #     raise forms.ValidationError('Password must be more than 8 character long')
        # if password and confirm_password and password != confirm_password:
        #     raise forms.ValidationError('Password mismatch')
        # if first_name.lower() in password.lower() or last_name.lower() in password.lower():
        #     raise forms.ValidationError('Password similar to name of user.')
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not re.match(r"[a-zA-Z]{3,30}", str(first_name)):
            raise forms.ValidationError('Invalid First Name')
        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name')

        if not re.match(r"[a-zA-Z]{3,30}", str(middle_name)):
            raise forms.ValidationError('Invalid Middle Name')
        return middle_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not re.match(r"[a-zA-Z]{3,30}", str(last_name)):
            raise forms.ValidationError('Invalid Last Name')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            raise forms.ValidationError('Invalid Email format')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if len(password1) < 8:
            raise forms.ValidationError('Password must be more than 8 character long')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch')
        return password2

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     # user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     print("user",user)
    #     # email_celery = json.dumps(user)
    #     # send_mail_func.delay(instance=User.objects.filter(pk=user.pk).values('email'))
    #     return user


class PasswordResetForm(forms.Form):
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your current password'}),
        strip=False,
    )

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        strip=False,
    )

    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise forms.ValidationError('Incorrect current password')
        return current_password

    def clean_new_password(self):
        current_password = self.cleaned_data.get('current_password')
        new_password = self.cleaned_data.get('new_password')

        if current_password == new_password:
            raise forms.ValidationError('current password is similar to the new password')
        return new_password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError('Both Password does not match!')
        return confirm_new_password


    
    def save(self, commit=True):
        password = self.cleaned_data.get('confirm_new_password')
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class UserRegisterFormByAdmin(forms.ModelForm):
    """
    Form to register a new user
    """
    class Meta:
        model = User
        fields = ['first_name', "middle_name", "last_name",'username', 'email', 'password','roles']