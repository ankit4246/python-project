from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, CreateView, DeleteView

from project.forms import ProjectDetailsForm, ProjectUsersForm, ProjectTargetForm
from project.models import Project, TargetType, ProjectTargets


class ListProjectsView(ListView):
    # ordering = ['-date_created']
    model = Project
    paginate_by = 5
    template_name = 'project/list_projects.html'


class ProjectDetailsView(View):
    template_name = 'project/create_project_details.html'

    def get(self, request, *args, **kwargs):
        if 'project_id' in kwargs:
            try:
                current_project = Project.objects.get(pk=kwargs['project_id'])
            except Project.DoesNotExist:
                current_project = None
            project_details_form = ProjectDetailsForm(instance=current_project)
        else:
            project_details_form = ProjectDetailsForm()

        context = {
            'project_details_form': project_details_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'project_id' in kwargs:
            try:
                current_project = Project.objects.get(pk=kwargs['project_id'])
            except Project.DoesNotExist:
                current_project = None
            project_details_form = ProjectDetailsForm(request.POST, request.FILES, instance=current_project)
        else:
            project_details_form = ProjectDetailsForm(request.POST, request.FILES)

        if project_details_form.is_valid():
            created_form = project_details_form.save(commit=False)
            created_form.created_by = request.user
            created_form.save()
            return redirect(reverse('project:create_project_targets',
                                    kwargs={'project_id': created_form.id}))
        context = {
            'project_details_form': project_details_form,
        }
        return render(request, self.template_name, context)


class ProjectTargetsView(View):
    template_name = 'project/create_project_targets.html'

    def get(self, request, *args, **kwargs):
        # try:
        #     current_project = Project.objects.get(pk=kwargs['project_id'])
        # except Project.DoesNotExist:
        #     current_project = None
        # if current_project is None:
        #     return redirect(reverse('page_not_found')
        project_target_form = ProjectTargetForm()
        context = {
            'project_target_form': project_target_form,
            'project_targets': ProjectTargets.objects.filter(project=kwargs['project_id']),
            'project_id': kwargs['project_id'],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        project_target_form = ProjectTargetForm(request.POST)
        try:
            current_project = Project.objects.get(pk=kwargs['project_id'])
        except Project.DoesNotExist:
            current_project = None
        context = {
            'project_target_form': project_target_form,
            'project_targets': ProjectTargets.objects.filter(project=kwargs['project_id']),
            'project_id': kwargs['project_id'],
        }
        if project_target_form.is_valid():
            created_form = project_target_form.save(commit=False)
            created_form.project = current_project
            created_form.save()
            return render(request, self.template_name, context)
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
class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("project:list_projects")
    success_message = "Deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ProjectTargetDeleteView(DeleteView):
    model = ProjectTargets
    success_message = "Deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        try:
            current_project_target = ProjectTargets.objects.get(id=self.kwargs['pk'])
        except ProjectTargets.DoesNotExist:
            current_project_target = None
        return reverse('project:create_project_targets',
                       kwargs={'project_id': current_project_target.project.id})
