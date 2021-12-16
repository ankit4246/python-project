from django import forms

from project.models import Project, ProjectUsers, Severity, Reward


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'logo',
            'project_name',
            'launched_date',
            'short_description',
            'description',
            'bounty_policies',
            'scope',
            'information',
            'disclosure_policies',
            'task_description',
            'target',
        ]
        widgets = {
            'launched_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'short_description': forms.widgets.Textarea(attrs={'rows': '5'}),
            'description': forms.widgets.Textarea(attrs={'rows': '5'}),
            'bounty_policies': forms.widgets.Textarea(attrs={'rows': '5'}),
            'information': forms.widgets.Textarea(attrs={'rows': '5'}),
            'disclosure_policies': forms.widgets.Textarea(attrs={'rows': '5'}),
            'task_description': forms.widgets.Textarea(attrs={'rows': '5'}),
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
