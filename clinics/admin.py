from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Department, DoctorProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'development_stage', 'get_doctors_count']

admin.site.register(DoctorProfile)