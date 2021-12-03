from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, UpdateView
from roles.models import Role
from users.decorators import permissions_in_menu_required
from users.forms.management_forms import UserRegisterFormByAdmin
from users.models import (User)
from users.tasks import send_invitation_mail
from users.utils import generate_invitation_token


@method_decorator(permissions_in_menu_required('User Management', ['can_view']), name='dispatch')
class UserListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "users/management/list_users.html"


@method_decorator(permissions_in_menu_required('User Management', ['can_add']), name='dispatch')
class UserCreateView(View):
    template_name = "users/management/user_create.html"

    def get(self, request, *args, **kwargs):
        form = UserRegisterFormByAdmin()
        context = {"form": form, "roles": Role.objects.all()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pwd = User.objects.make_random_password(length=8)
        print(request.POST)
        updated_request = request.POST.copy()
        updated_request.update({"password": pwd})
        form = UserRegisterFormByAdmin(updated_request)
        print("before valid")
        if form.is_valid():
            print("after valid")
            user = form.save(commit=False)
            user.set_password(pwd)
            user.save()
            token = generate_invitation_token(form.instance.id)
            send_invitation_mail.delay(email=form.instance.email, token=str(token), pwd=pwd)
            return redirect(reverse_lazy('users:list_user'))
        print("outside valid")
        print(form.errors)
        context = {
            'form': form,
            "roles": Role.objects.all()
        }
        return render(request, self.template_name, context)


@method_decorator(permissions_in_menu_required('User Management', ['can_change']), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = "users/management/user_update.html"
    fields = ["first_name", "middle_name", "last_name", "username", "roles"]
    success_url = reverse_lazy("users:list_user")
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Role.objects.all()
        return context


@method_decorator(permissions_in_menu_required('User Management', ['can_delete']), name='dispatch')
def user_delete_view(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.success(request, "A user has been deleted.")
    return redirect('users:list_user')


@method_decorator(permissions_in_menu_required('User Management', ['can_delete']), name='dispatch')
def user_deactivate(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        user.is_active = False
        user.save()
        messages.success(request, " User account has been successfully deactivated! ")
        return redirect("users:list_user")


@method_decorator(permissions_in_menu_required('User Management', ['can_delete']), name='dispatch')
def user_activate(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        user.is_active = True
        user.save()
        messages.success(request, " User account has been successfully activated! ")
        return redirect("users:list_user")
