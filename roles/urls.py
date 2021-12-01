from django.urls import path

from roles.views import (
    AssignRolePermissionsView,
    RoleCreateView,
    # RoleDeleteView,
    RoleListView,
    RolePermissionSetupView,
    RoleUpdateView, role_delete_view,
)

# app_name = "roles"
urlpatterns = [
    path("", RoleListView.as_view(), name="list_role"),
    path("setup/<int:role_id>/", RolePermissionSetupView.as_view(), name="role_setup"),
    path("create/", RoleCreateView.as_view(), name="role_create"),
    path("<int:pk>/update/", RoleUpdateView.as_view(), name="role_update"),
    # path("<int:pk>/delete/", RoleDeleteView.as_view(), name="role_delete"),
    path("<int:pk>/delete/", role_delete_view, name="role_delete"),
    path(
        "assign/perm/<int:menu_id>/<int:role_id>/",
        AssignRolePermissionsView.as_view(),
        name="assign_perm",
    ),
]
