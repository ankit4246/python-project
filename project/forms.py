from django import forms

from project.models import Project


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

