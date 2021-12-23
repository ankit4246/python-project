from django import forms

from project.models import Project, ProjectUsers, Severity, Reward, TargetType, ProjectTargets


class ProjectDetailsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'logo',
            'project_name',
            'tagline',
            'objectives',
            'policies',
            'budget',
            'created_by',
            'is_draft',
            'is_published',
            'start_date',
            'end_date',
        ]
        widgets = {
            'logo': forms.widgets.FileInput(attrs={'class': 'form-control'}),
            'project_name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'objectives': forms.widgets.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
            'policies': forms.widgets.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
        }


class ProjectUsersForm(forms.ModelForm):
    class Meta:
        model = ProjectUsers
        fields = [
            'user',
            'project',
            'project_role',
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'id': 'user-id'}),
        }


class ProjectTargetForm(forms.ModelForm):
    class Meta:
        model = ProjectTargets
        fields = [
            'url',
            'target',
            'project',
        ]
        widgets = {
            'url': forms.widgets.URLInput(attrs={'class': 'form-control'}),
            'target': forms.widgets.Select(attrs={'id': 'Website'}),
        }


class SeverityForm(forms.ModelForm):
    class Meta:
        model = Severity
        fields = [
            'name',
        ]


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = [
            'low',
            'high',
            'severity',
            'project',
        ]
