from roles.models import MenuPermission


def get_user_perm(user, menu):
    return MenuPermission.objects.filter(menu=menu, role__users=user).distinct()


def admin(u):
    return u.is_superuser


def menu_permissions_create(role, menu, role_perms):
    # add menu inside role
    role.menus.add(menu)
    # update menu permissions
    MenuPermission.objects.update_or_create(menu=menu, role=role)
    MenuPermission.objects.filter(menu=menu, role=role).update(**role_perms)
    # if menu has parent, add parent menu as well to the role and give can view permission by default
    if menu.parent:
        role.menus.add(menu.parent)
        MenuPermission.objects.update_or_create(
            menu=menu.parent, role=role, can_view=True
        )


def menu_permissions_remove(role, menu):
    # remove menu permissions
    role.menu_permissions.filter(menu=menu).delete()
    # remove menus from role
    role.menus.remove(menu)
    if menu.parent:
        children = menu.parent.children.all()
        # if parent menu doesn't have any children inside role remove the parent menu from role as well
        if not role.menus.filter(id__in=children).exists():
            role.menus.remove(menu.parent)
            role.menu_permissions.filter(menu=menu.parent).delete()
