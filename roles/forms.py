from django import forms

from roles.models import MenuPermission


class RolePermissionSetupForm(forms.ModelForm):
    class Meta:
        model = MenuPermission
        fields = ["can_add", "can_change", "can_delete", "can_view", "can_approve"]