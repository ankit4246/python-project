from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, View
from django.views.generic.edit import DeleteView, UpdateView
from roles.forms import RolePermissionSetupForm
from roles.models import Menu, MenuPermission, Role
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from roles.utils import menu_permissions_create, menu_permissions_remove
from django.db.models import Case, When, IntegerField, Count
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


class RoleListView(ListView):
    model = Role
    context_object_name = "roles"
    template_name = "roles/role_list.html"


class RoleCreateView(SuccessMessageMixin, CreateView):
    model = Role
    fields = ["name", "desc"]
    template_name = "roles/role_create.html"
    success_url = reverse_lazy("roles:list_role")
    success_message = "Created Successfully."

    def get_success_url(self):
        if "perm-setup" in self.request.POST:
            # redirect to permission setup if button with name `perm-setup` clicked
            role_id = self.object.id
            return reverse("roles:role_setup", args=(role_id,))
        return super().get_success_url()


class RoleUpdateView(SuccessMessageMixin, UpdateView):
    model = Role
    fields = ["name", "desc"]
    template_name = "roles/role_update.html"
    success_url = reverse_lazy("roles:list_role")
    success_message = "Updated Successfully."


class RoleDeleteView(DeleteView):
    model = Role
    success_url = reverse_lazy("roles:list_role")


class RolePermissionSetupView(View):
    template_name = "roles/role_menu_setup.html"

    def get(self, request, *args, **kwargs):
        role_qs = Role.objects.all()
        role = Role.objects.get(id=kwargs["role_id"])
        menu_qs = Menu.objects.exclude(children__isnull=False)
        # list menus inside the role first and then order with order_id
        role_menus = role.menus.exclude(children__isnull=False)
        menus = (
            menu_qs.annotate(
                order=Case(
                    When(pk__in=role_menus, then=0),
                    default=1,
                    output_field=IntegerField(),
                )
            )
            .order_by("order", "order_id")
            .distinct()
        )

        context = {
            "roles": role_qs,
            "role": role,
            "menus": menus,
            "kwargs_id": kwargs.get("role_id"),
        }
        return render(request, self.template_name, context)


class AssignRolePermissionsView(View):
    """assign menu permissions inside user role"""

    def post(self, request, *args, **kwargs):
        form = RolePermissionSetupForm(request.POST)
        if form.is_valid():
            menu = Menu.objects.get(id=kwargs["menu_id"])
            role = Role.objects.get(id=kwargs["role_id"])
            role_perms = {
                "can_add": form.cleaned_data.get("can_add", 0),
                "can_change": form.cleaned_data.get("can_change", 0),
                "can_view": form.cleaned_data.get("can_view", 0),
                "can_delete": form.cleaned_data.get("can_delete", 0),
            }
            with transaction.atomic():
                if 1 in role_perms.values():
                    menu_permissions_create(role, menu, role_perms)
                else:
                    menu_permissions_remove(role, menu)
                return JsonResponse({"success": True})
        return HttpResponse(f"Invalid Data. Errors:{form.errors}")
