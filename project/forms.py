from django import forms

from project.models import Project, ProjectUsers, Severity, Reward


class ProjectForm(forms.ModelForm):
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
            'target',
            'is_draft',
            'is_published',
            'start_date',
            'end_date',
        ]
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'objectives': forms.widgets.Textarea(attrs={'rows': '5'}),
            'policies': forms.widgets.Textarea(attrs={'rows': '5'}),
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
