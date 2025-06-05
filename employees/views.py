from django.shortcuts import render ,redirect,get_object_or_404
from .models import Employee 
from .forms import EmployeeForm,CustomUserForm
from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.

from django.contrib.auth import authenticate, login, get_user_model

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Note: pass email as 'username' param
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'employees/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserForm()
        print(form.errors)
    
    return render(request, 'employees/register.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('login')
    else:
        return redirect('login')


@login_required(login_url='login')
def home(request):
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='active').count()
    inactive_employees = Employee.objects.filter(status='inactive').count()
    on_leave_employees = Employee.objects.filter(status='on_leave').count()
    employees = Employee.objects.all().order_by('last_name', 'first_name')
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'on_leave_employees': on_leave_employees,
        'employees': employees,
    }
    return render(request, 'employees/home.html', context)


@login_required(login_url='login')
def add_employee(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to add employees.")
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('home')
    else:
        print(form.errors)
    
    return render(request, 'employees/add_employee.html', {'form': form})

@login_required(login_url='login')
def delete_employee(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to add employees.")
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('home')

    return render(request, 'employees/deleteAlert.html', {'employee': employee})

@login_required(login_url='login')
def profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/profileEmployee.html', {'employee': employee})


@login_required(login_url='login')
def edit_employee(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to delete employees.")
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'employees/updateEmployee.html', {'form': form, 'employee': employee})


