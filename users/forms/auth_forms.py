import re

from django import forms

from users.models import User


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
