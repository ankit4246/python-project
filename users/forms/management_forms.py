from django import forms

from users.models import User


class UserRegisterFormByAdmin(forms.ModelForm):
    """
    Form to register a new user
    """

    class Meta:
        model = User
        fields = ['first_name', "middle_name", "last_name", 'username', 'email', 'password', 'roles']
