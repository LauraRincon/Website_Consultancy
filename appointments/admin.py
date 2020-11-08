from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Client, Project

# Register your models here.
admin.site.register(Client, UserAdmin)
admin.site.register(Project)
