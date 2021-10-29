from django.forms import ModelForm

from users.models import Profile, TrainingDetails, ExperienceDetails, SocialMedias


class BasicInformation(ModelForm):
    class Meta:
        model = Profile


class TrainingForm(ModelForm):
    class Meta:
        model = TrainingDetails


class ExperienceForm(ModelForm):
    class Meta:
        model = ExperienceDetails


class SocialMediaForm(ModelForm):
    class Meta:
        model = SocialMedias
