from django.db import models

# Create your models here.
from pentest.models import TimeStamp
from users.models import User


class Role(models.Model):
    role_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)


class Severity(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class TargetType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Project(TimeStamp):
    logo = models.ImageField(blank=True, null=True, upload_to='logos/')
    project_name = models.CharField(max_length=100, blank=True, null=True)
    tagline = models.CharField(max_length=100, blank=True, null=True)
    objectives = models.CharField(max_length=600, blank=True, null=True)
    policies = models.CharField(max_length=600, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='created_by')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name


class ProjectTargets(models.Model):
    url = models.URLField()
    target = models.ForeignKey(TargetType, models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)


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

    def __str__(self):
        return self.user.first_name


class ReportType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    types = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Reward(models.Model):
    low = models.IntegerField()
    high = models.IntegerField()
    severity = models.ForeignKey(Severity, models.DO_NOTHING)
    project = models.ForeignKey(Project, models.DO_NOTHING)
