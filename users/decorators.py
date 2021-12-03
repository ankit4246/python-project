from django.contrib.auth.decorators import user_passes_test

from roles.models import MenuPermission, Role


# def roles_required(*role_names):
#     """Requires user membership in at least one of the groups passed in."""
#
#     def in_groups(u):
#         if u.is_authenticated:
#             user_roles = u.roles.filter(name__in=role_names)
#             if user_roles or u.is_superuser:
#                 return True
#         return False
#
#     return user_passes_test(in_groups)


def get_roles_from_menu_and_permissions(menu_name, permission_names):
    menu_permissions_for_menu = MenuPermission.objects.filter(menu__name=menu_name)
    required_menu_permissions = []
    for menu_permission in menu_permissions_for_menu:
        for permission_name in permission_names:
            if permission_name == 'can_add' and menu_permission.can_add == True:
                required_menu_permissions.append(menu_permission)
            if permission_name == 'can_view' and menu_permission.can_view == True:
                required_menu_permissions.append(menu_permission)
            if permission_name == 'can_change' and menu_permission.can_change == True:
                required_menu_permissions.append(menu_permission)
            if permission_name == 'can_delete' and menu_permission.can_delete == True:
                required_menu_permissions.append(menu_permission)
    required_menu_permissions_set = set(required_menu_permissions)

    role_names_queryset = Role.objects.filter(menu_permissions__in=required_menu_permissions_set)
    role_names = []
    for role_name in role_names_queryset:
        role_names.append(role_name)
        
    return role_names


def permissions_in_menu_required(menu_name, permission_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated:
            # roles = u.roles.filter(menus__in=menu_name)
            role_names = get_roles_from_menu_and_permissions(menu_name, permission_names)
            user_roles = u.roles.filter(name__in=role_names)
            if user_roles or u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)
