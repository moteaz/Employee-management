# forms.py
from django import forms
from .models import Employee  # assuming you have an Employee model


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'job_title', 'status']

