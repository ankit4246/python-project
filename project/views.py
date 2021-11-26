from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from project.models import Project


class ListProjectsView(ListView):
    model = Project
    paginate_by = 3
    template_name = 'project/list_projects.html'


# class CreateProjectView(CreateView):
