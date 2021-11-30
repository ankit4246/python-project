from django.contrib import admin

# Register your models here.
from roles.models import Menu, MenuPermission, Role

admin.site.register([Menu, MenuPermission, Role])
