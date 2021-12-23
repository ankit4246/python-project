from django.shortcuts import render
from master_data.forms import SeverityForm, TargetTypeForm, ReportTypeForm, DistrictForm, ProvinceForm, DegreeForm
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from project.models import Severity, TargetType, ReportType
from users.models import Province, District, Degree
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse


# For CRUD Severity
# class SeverityCreateView(SuccessMessageMixin, CreateView):
#     model = Severity
#     form_class = SeverityForm
#     template_name = "master_data/create_master_data.html"
#     success_url = reverse_lazy('master_data:severity_list')
#     success_message = "Severity Created successfully"

# class SeverityListView(ListView):
#     model = Severity
#     template_name = "master_data/list_master_data.html"
#     ordering = ['-id']
#     context_object_name = "severity"

# class SeverityUpdateView(SuccessMessageMixin, UpdateView):
#     model = Severity
#     form_class = SeverityForm
#     template_name = "master_data/update_master_data.html"
#     success_url = reverse_lazy('master_data:severity_list')
#     success_message = "Severity Updated successfully"
# class SeverityDeleteView(DeleteView):
#     model = Severity
#     success_url = reverse_lazy('master_data:severity_list')
#     success_message = "Deleted successfully."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


def severityCreateView(request):
    form = SeverityForm
    severity = Severity.objects.all().order_by('-id')
    return render(request, 'master_data/severity.html', {"form":form, "severity":severity,})

# ajax function
def severitySaveView(request):
    if request.method == "POST":
        form = SeverityForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            remarks = request.POST['remarks']
            sid = request.POST.get('sid')

            if (sid == ""):
                severity = Severity(name=name, remarks=remarks)
            else:
                severity = Severity(id=sid, name=name, remarks=remarks)
            severity.save()

            sv = Severity.objects.values().order_by("-id") #important
            severity_data = list(sv)
            return JsonResponse({"status": "Save", 'severity_data': severity_data, })
        else:
            return JsonResponse({"status": 0})


def severityUpdateView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        severity = Severity.objects.get(pk=id)
        severity_data = {"id": severity.id, 'name': severity.name, 'remarks': severity.remarks}
        return JsonResponse(severity_data)


def severityDeleteView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        severity = Severity.objects.get(pk=id)
        severity.delete()
        sv = Severity.objects.values().order_by("-id") #important
        severity_data = list(sv)
        return JsonResponse({'status':1, 'severity_data':severity_data,})
    else:
        return JsonResponse({'status': 0})
