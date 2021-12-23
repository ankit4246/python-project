from django import forms
from project.models import Severity, TargetType, ReportType
from users.models import Province, District, Degree


class SeverityForm(forms.ModelForm):
    class Meta:
        model = Severity
        fields = ["name", "remarks"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'nameid'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'remarksid'}),
        }


class TargetTypeForm(forms.ModelForm):
    class Meta:
        model = TargetType
        fields = ["name", "remarks"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'nameid'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'remarksid'}),
        }

class ReportTypeForm(forms.ModelForm):
    class Meta:
        model = ReportType
        fields = ["name", "types", "remarks"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'nameid'}),
            'types': forms.TextInput(attrs={'class': 'form-control', 'id': 'typesid'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'remarksid'}),
        }

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
        fields = ["name", "types", "remarks"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'nameid'}),
            'types': forms.TextInput(attrs={'class': 'form-control', 'id': 'typesid'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'remarksid'}),
        }
