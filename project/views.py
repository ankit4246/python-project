from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, FormView

from project.forms import ProjectForm
from project.models import Project


class ListProjectsView(ListView):
    model = Project
    paginate_by = 5
    template_name = 'project/list_projects.html'


class CreateProjectView(View):
    form_class = ProjectForm
    template_name = 'project/create_project.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('project:list_projects'))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)



