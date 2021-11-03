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
