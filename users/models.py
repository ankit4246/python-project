from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
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

    class Meta:
        managed = False


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    username = models.CharField(max_length=100)
    # email_address_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # password = models.CharField(max_length=255)
    # skills = models.ManyToManyField(Skills, blank=True)

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


class AddressDetails(models.Model):
    address = models.CharField(max_length=150, blank=True, null=True)
    province = models.ForeignKey('Province', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey('District', models.DO_NOTHING, blank=True, null=True)
    ward_no = models.IntegerField(blank=True, null=True)
    tole = models.CharField(max_length=100, blank=True, null=True)
    house_no = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False


class Country(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False


class District(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False


class EducationDetails(models.Model):
    university = models.ForeignKey('University', models.DO_NOTHING, blank=True, null=True)
    edu_level = models.CharField(max_length=150, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    per_gpa_type = models.CharField(max_length=100, blank=True, null=True)
    per_gpa_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    passed_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False


class ExperienceDetails(models.Model):
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    job_level = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    jd = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False


class Province(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False


class TrainingDetails(models.Model):
    name_of_training = models.CharField(max_length=255, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    duration_type = models.CharField(max_length=100, blank=True, null=True)
    completion_month = models.CharField(max_length=30, blank=True, null=True)
    completion_year = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False


class University(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    short_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False


class Profile(models.Model):
    father_full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_full_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_full_name = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    national_identity_num = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False


class SocialMedias(models.Model):
    social_media = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    profile = models.ForeignKey(Profile, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False

# class UsersSkills(models.Model):
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
#     skill = models.ForeignKey(Skills, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'users_skills'

# class LoginCred(models.Model):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#     )
#     password = models.CharField(max_length=50)