from django.forms import ModelForm

from users.models import Profile


class BasicInformation(ModelForm):
    class Meta:
        model = Profile
