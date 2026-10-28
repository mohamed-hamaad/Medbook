from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )
    
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']

admin.site.register(User, CustomUserAdmin)