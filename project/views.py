from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, FormView, CreateView

from project.forms import ProjectForm, ProjectUsersForm
from project.models import Project


class ListProjectsView(ListView):
    model = Project
    paginate_by = 5
    template_name = 'project/list_projects.html'


class CreateProjectView(View):
    template_name = 'project/create_project_details.html'

    def get(self, request, *args, **kwargs):
        project_form = ProjectForm()

        context = {
            'project_form': project_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            created_form = project_form.save(commit=False)
            created_form.created_by = request.user
            created_form.save()
            return redirect(reverse('project:list_projects'))
        context = {
            'project_form': project_form,
        }
        return render(request, self.template_name, context)


def create_project_users_view(request):
    project_users_form = ProjectUsersForm(request.POST)
    if project_users_form.is_valid():
        project_users_form.save()
        return JsonResponse({"status": "Save"})
    return JsonResponse({"status": 0})


class ListProjectView(ListView):
    form_class = ProjectUsersForm
    template_name = 'project/create_project_details.html'

# class VehicleManufacturerCreateView(SuccessMessageMixin, CreateView):
#     model = Manufacturer
#     fields = [
#         "name",
#     ]
#     template_name = "core/vehiclemanufacturer/vehiclemanufacturer_create.html"
#     success_url = reverse_lazy("core:vehiclemanufacturer-list")
#     success_message = "VehicleManufacturer created successfully"
