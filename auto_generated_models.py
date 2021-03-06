# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddressDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    province = models.ForeignKey('Province', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey('District', models.DO_NOTHING, blank=True, null=True)
    ward_no = models.IntegerField(blank=True, null=True)
    tole = models.CharField(max_length=-1, blank=True, null=True)
    house_no = models.CharField(max_length=-1, blank=True, null=True)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address_details'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bugs(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=-1, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    bug_reporter = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='bug_reporter', blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bugs'


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country'


class District(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EducationDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    university = models.ForeignKey('University', models.DO_NOTHING, blank=True, null=True)
    edu_level = models.CharField(max_length=150, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    per_gpa_type = models.CharField(max_length=-1, blank=True, null=True)
    per_gpa_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    passed_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education_details'


class ExperienceDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    job_level = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    jd = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experience_details'


class ProjectRoles(models.Model):
    id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_roles'


class Projects(models.Model):
    id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=-1, blank=True, null=True)
    scope = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class ProjectsUsers(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(Projects, models.DO_NOTHING, blank=True, null=True)
    project_role = models.ForeignKey(ProjectRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects_users'


class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'province'


class Skills(models.Model):
    id = models.IntegerField(primary_key=True)
    skill = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'


class Test(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'test'


class TrainingDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    name_of_training = models.CharField(max_length=255, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    duration_type = models.CharField(max_length=-1, blank=True, null=True)
    completion_month = models.CharField(max_length=30, blank=True, null=True)
    completion_year = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'training_details'


class University(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    short_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'university'


class UserProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    father_full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_full_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_full_name = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    national_identity_num = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'


class UserSocialMedias(models.Model):
    id = models.IntegerField(primary_key=True)
    social_media = models.CharField(max_length=-1, blank=True, null=True)
    link = models.CharField(max_length=-1, blank=True, null=True)
    profile = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_social_medias'


class UsersSkills(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    skill = models.ForeignKey(Skills, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_skills'
