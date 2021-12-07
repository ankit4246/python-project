from django import forms
from project.models import Severity, TargetType, ReportType
from users.models import Province, District, Degree

class SeverityForm(forms.ModelForm):
    
    class Meta:
        model = Severity
        fields = ["name", "remarks"]


class TargetTypeForm(forms.ModelForm):
    
    class Meta:
        model = TargetType
        fields = ["name", "remarks"]

class ReportTypeForm(forms.ModelForm):

    class Meta:
        model = ReportType
        fields = ["name", "types", "remarks"]

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ["name"]

class ProvinceForm(forms.ModelForm):

    class Meta:
        model = Province
        fields = ["name"]

class DegreeForm(forms.ModelForm):

    class Meta:
        model = Degree
        fields = ["types", "name", "remarks"]