from django.contrib import admin
from project.models import Project, Severity, Role, TargetType, Bug, ProjectUsers, ReportType, Reward

# Register your models here.
admin.site.register(Role)
admin.site.register(Severity)
admin.site.register(TargetType)
admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(ProjectUsers)
admin.site.register(ReportType)
admin.site.register(Reward)
