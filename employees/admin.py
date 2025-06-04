from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'job_title', 'status')
    search_fields = ('first_name', 'last_name', 'email', 'job_title')
    list_filter = ('job_title', 'status')
    ordering = ('last_name', 'first_name')
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Job Details', {
            'fields': ('job_title', 'status'),
            'classes': ('collapse',),
        }),
    )
