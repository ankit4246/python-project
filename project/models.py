from django.db import models

# Create your models here.
from users.models import User


class Role(models.Model):
    role_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)


class Project(models.Model):
    project_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    scope = models.CharField(max_length=100, blank=True, null=True)
    information = models.CharField(max_length=250, blank=True, null=True)
    team_lead_id = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='team_lead')
    created_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='created_by')

class Bug(models.Model):
    description = models.CharField(max_length=250, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    bug_reporter = models.ForeignKey(User, models.DO_NOTHING, db_column='bug_reporter', blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)


class ProjectUsers(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    project_role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)

class Severity(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=100, blank=100)

    def __str__(self):
        return self.name

class TargetType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=100, blank=100)

    def __str__(self):
        return self.name
    

class ReportType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    types = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=100, blank=100)

    def __str__(self):
        return self.name