from django import template
from roles.models import Menu, MenuPermission
from roles.utils import admin

register = template.Library()


def menu_perms(u, menu_code):
    if u.is_authenticated:
        return MenuPermission.objects.filter(menu__code=menu_code, role__users=u)
    return MenuPermission.objects.none()


@register.simple_tag
def user_can_change(request, code):
    """returns True if user has the permission for update otherwise False"""
    u = request.user
    can_change = menu_perms(u, code).filter(can_change=True).exists()
    return admin(u) or can_change


@register.simple_tag
def user_can_add(request, code):
    u = request.user
    can_add = menu_perms(request.user, code).filter(can_add=True).exists()
    return admin(u) or can_add


@register.simple_tag
def user_can_view(request, code):
    u = request.user
    can_view = menu_perms(u, code).filter(can_view=True).exists()
    return admin(u) or can_view


@register.simple_tag
def user_can_delete(request, code):
    u = request.user
    can_delete = menu_perms(u, code).filter(can_delete=True).exists()
    return admin(u) or can_delete
