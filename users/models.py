from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from roles.models import Role

MONTH_CHOICES = [('1', 'January'),
                 ('2', 'February'),
                 ('3', 'March'),
                 ('4', 'April'),
                 ('5', 'May'),
                 ('6', 'June'),
                 ('7', 'July'),
                 ('8', 'August'),
                 ('9', 'September'),
                 ('10', 'October'),
                 ('11', 'November'),
                 ('12', 'December'),
                 ]
import datetime

YEAR_CHOICES = []
for r in range(1960, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Skills(models.Model):
    skill = models.CharField(max_length=100, blank=True, null=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    username = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skills, blank=True)
    roles = models.ManyToManyField(Role, blank=True, related_name="users")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_user_roles(self):
        # returns comma separted role names of user
        roles = self.roles.values_list("name", flat=True)
        if self.is_superuser:
            return "Superuser"
        return ", ".join(roles)


class AddressDetails(models.Model):
    address = models.CharField(max_length=150, blank=True, null=True)
    province = models.ForeignKey('Province', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey('District', models.DO_NOTHING, blank=True, null=True)
    local_body = models.CharField(max_length=100, blank=True, null=True)  ############################
    mobile_no = models.CharField(max_length=20, blank=True, null=True)  ##########################
    ward_no = models.IntegerField(blank=True, null=True)
    tole = models.CharField(max_length=100, blank=True, null=True)
    house_no = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)


class Country(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class EducationDetails(models.Model):
    university = models.ForeignKey('University', models.DO_NOTHING, blank=True, null=True)
    edu_level = models.CharField(max_length=150, blank=True, null=True)
    faculty = models.CharField(max_length=150, blank=True, null=True)
    institution_name = models.CharField(max_length=150, blank=True, null=True)
    per_gpa_type = models.CharField(max_length=100, blank=True, null=True)
    per_gpa_value = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    passed_month = models.CharField(max_length=2, blank=True, null=True)
    passed_year = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.institution_name


class ExperienceDetails(models.Model):
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    job_level = models.CharField(max_length=100, blank=True, null=True)
    start_month = models.CharField(max_length=2, blank=True, null=True)
    start_year = models.CharField(max_length=4, blank=True, null=True)
    is_current = models.BooleanField(blank=True, null=True)
    jd = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)


class Province(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name


class TrainingDetails(models.Model):
    name_of_training = models.CharField(max_length=255, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    duration_type = models.CharField(max_length=100, blank=True, null=True)
    completion_month = models.CharField(max_length=2, blank=True, null=True)
    completion_year = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)


class University(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    short_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    father_full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_full_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_full_name = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    national_identity_num = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)


class SocialMedias(models.Model):
    social_media = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
