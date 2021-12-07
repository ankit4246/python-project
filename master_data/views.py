from django.shortcuts import render
from master_data.forms import SeverityForm, TargetTypeForm, ReportTypeForm, DistrictForm, ProvinceForm, DegreeForm
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from project.models import Severity, TargetType, ReportType
from users.models import Province, District, Degree
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

# For CRUD Severity
class SeverityCreateView(SuccessMessageMixin, CreateView):
    model = Severity
    form_class = SeverityForm
    template_name = "master_data/create_master_data.html"
    success_url = reverse_lazy('master_data:severity_list')
    success_message = "Severity Created successfully"

class SeverityListView(ListView):
    model = Severity
    template_name = "master_data/list_master_data.html"
    ordering = ['-id']
    context_object_name = "severity"

class SeverityUpdateView(SuccessMessageMixin, UpdateView):
    model = Severity
    form_class = SeverityForm
    template_name = "master_data/update_master_data.html"
    success_url = reverse_lazy('master_data:severity_list')
    success_message = "Severity Updated successfully"
class SeverityDeleteView(DeleteView):
    model = Severity
    success_url = reverse_lazy('master_data:severity_list')
    success_message = "Deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
