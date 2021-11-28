from roles.models import Menu


def get_dashboard_menus(request):
    all_menus = Menu.objects.all()
    parent_menus = all_menus.filter(parent=None)
    u = request.user
    if u.is_authenticated and not u.is_superuser:
        # filter user's menus based on user roles and permissions
        u_roles = u.roles.all()
        qs = all_menus.filter(permissions__role__in=u_roles, permissions__can_view=True)
        parent_menus = qs.filter(parent=None)
        all_menus = qs

    return {"parent_menus": parent_menus, "all_menus": all_menus}
