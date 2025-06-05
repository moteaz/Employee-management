# forms.py
from django import forms
from .models import Employee,User  # assuming you have an Employee model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import uuid

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'job_title', 'status']



class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']

        # Generate a unique username (required by Django)
        user.username = str(uuid.uuid4())  # or email if guaranteed unique
        user.email = email

        # Split full name
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''

        if commit:
            user.save()
        return user


