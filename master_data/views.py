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

# For severity
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





# For TargetType
def targetTypeCreateView(request):
    form = TargetTypeForm
    target = TargetType.objects.all().order_by('-id')
    return render(request, 'master_data/target.html', {"form":form, "target":target,})

# ajax function
def targetTypeSaveView(request):
    if request.method == "POST":
        form = TargetTypeForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            remarks = request.POST['remarks']
            sid = request.POST.get('sid')

            if (sid == ""):
                target = TargetType(name=name, remarks=remarks)
            else:
                target = TargetType(id=sid, name=name, remarks=remarks)
            target.save()

            sv = TargetType.objects.values().order_by("-id") #important
            target_data = list(sv)
            return JsonResponse({"status": "Save", 'target_data': target_data, })
        else:
            return JsonResponse({"status": 0})


def targetTypeUpdateView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        target = TargetType.objects.get(pk=id)
        target_data = {"id": target.id, 'name': target.name, 'remarks': target.remarks}
        return JsonResponse(target_data)


def targetTypeDeleteView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        target = TargetType.objects.get(pk=id)
        target.delete()
        sv = TargetType.objects.values().order_by("-id") #important
        target_data = list(sv)
        return JsonResponse({'status':1, 'target_data':target_data,})
    else:
        return JsonResponse({'status': 0})



# For ReportType
def reportTypeCreateView(request):
    form = ReportTypeForm
    report = ReportType.objects.all().order_by('-id')
    return render(request, 'master_data/report.html', {"form":form, "report":report,})

# ajax function
def reportTypeSaveView(request):
    if request.method == "POST":
        form = ReportTypeForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            types = request.POST['types']
            remarks = request.POST['remarks']
            sid = request.POST.get('sid')

            if (sid == ""):
                report = ReportType(name=name, types=types, remarks=remarks)
            else:
                report = ReportType(id=sid, types=types, name=name, remarks=remarks)
            report.save()

            sv = ReportType.objects.values().order_by("-id") #important
            report_data = list(sv)
            return JsonResponse({"status": "Save", 'report_data': report_data, })
        else:
            return JsonResponse({"status": 0})


def reportTypeUpdateView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        report = ReportType.objects.get(pk=id)
        report_data = {"id": report.id, 'name': report.name, 'types': report.types, 'remarks': report.remarks}
        return JsonResponse(report_data)


def reportTypeDeleteView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        report = ReportType.objects.get(pk=id)
        report.delete()
        sv = ReportType.objects.values().order_by("-id") #important
        report_data = list(sv)
        return JsonResponse({'status':1, 'report_data':report_data,})
    else:
        return JsonResponse({'status': 0})



# for Degree
def degreeCreateView(request):
    form = DegreeForm
    degree = Degree.objects.all().order_by('-id')
    return render(request, 'master_data/degree.html', {"form":form, "degree":degree,})

# ajax function
def degreeSaveView(request):
    if request.method == "POST":
        form = DegreeForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            types = request.POST['types']
            remarks = request.POST['remarks']
            sid = request.POST.get('sid')

            if (sid == ""):
                degree = Degree(name=name, types=types, remarks=remarks)
            else:
                degree = Degree(id=sid, name=name, types=types, remarks=remarks)
            degree.save()

            sv = Degree.objects.values().order_by("-id") #important
            degree_data = list(sv)
            return JsonResponse({"status": "Save", 'degree_data': degree_data, })
        else:
            return JsonResponse({"status": 0})


def degreeUpdateView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        degree = Degree.objects.get(pk=id)
        degree_data = {"id": degree.id, 'name': degree.name, 'types': degree.types, 'remarks': degree.remarks}
        return JsonResponse(degree_data)


def degreeDeleteView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        degree = Degree.objects.get(pk=id)
        degree.delete()
        sv = Degree.objects.values().order_by("-id") #important
        degree_data = list(sv)
        return JsonResponse({'status':1, 'degree_data':degree_data,})
    else:
        return JsonResponse({'status': 0})



# For Province
def provinceCreateView(request):
    form = ProvinceForm
    province = Province.objects.all().order_by('-id')
    return render(request, 'master_data/province.html', {"form":form, "province":province,})

# ajax function
def provinceSaveView(request):
    if request.method == "POST":
        form = ProvinceForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            sid = request.POST.get('sid')

            if (sid == ""):
                province = Province(name=name)
            else:
                province = Province(id=sid, name=name)
            province.save()

            sv = Province.objects.values().order_by("-id") #important
            province_data = list(sv)
            return JsonResponse({"status": "Save", 'province_data': province_data, })
        else:
            return JsonResponse({"status": 0})


def provinceUpdateView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        province = Province.objects.get(pk=id)
        province_data = {"id": province.id, 'name': province.name,}
        return JsonResponse(province_data)


def provinceDeleteView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        province = Province.objects.get(pk=id)
        province.delete()
        sv = Province.objects.values().order_by("-id") #important
        province_data = list(sv)
        return JsonResponse({'status':1, 'province_data':province_data,})
    else:
        return JsonResponse({'status': 0})



# For District
def districtCreateView(request):
    form = DistrictForm
    district = District.objects.all().order_by('-id')
    return render(request, 'master_data/district.html', {"form":form, "district":district,})

# ajax function
def districtSaveView(request):
    if request.method == "POST":
        form = DistrictForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            sid = request.POST.get('sid')

            if (sid == ""):
                district = District(name=name)
            else:
                district = District(id=sid, name=name)
            district.save()

            sv = District.objects.values().order_by("-id") #important
            district_data = list(sv)
            return JsonResponse({"status": "Save", 'district_data': district_data, })
        else:
            return JsonResponse({"status": 0})


def districtUpdateView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        district = District.objects.get(pk=id)
        district_data = {"id": district.id, 'name': district.name,}
        return JsonResponse(district_data)


def districtDeleteView(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        district = District.objects.get(pk=id)
        district.delete()
        sv = District.objects.values().order_by("-id") #important
        district_data = list(sv)
        return JsonResponse({'status':1, 'district_data':district_data,})
    else:
        return JsonResponse({'status': 0})
