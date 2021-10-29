from django.forms import ModelForm
from users.models import Profile, AddressDetails, EducationDetails


class BasicInformation(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class AddressInfo(ModelForm):
    class Meta:
        model = AddressDetails
        fields = '__all__'

class EducationInfo(ModelForm):
    class Meta:
        model = EducationDetails
        fields = '__all__'