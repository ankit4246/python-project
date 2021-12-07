from django.shortcuts import render
from master_data.forms import SeverityForm, TargetTypeForm, ReportTypeForm, DistrictForm, ProvinceForm, \
    DegreeForm
from django.views.generic import ListView, UpdateView, CreateView
from project.models import Severity, TargetType, ReportType,
from users.models import Province, District, Degree


class SeverityCreateView(CreateView):
    model = Severity
    form_class = SeverityForm
    template_name = "master_data"