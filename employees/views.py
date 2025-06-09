from django.shortcuts import render ,redirect,get_object_or_404
from .models import Employee 
from .forms import EmployeeForm
# from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Q

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'employees/login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

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

    departments = Employee.objects.values_list('job_title', flat=True).distinct()
    selected_dept = request.GET.get('department')
    selected_status = request.GET.get('status')
    search_query = request.GET.get('employee')

    employees = Employee.objects.all()

    if selected_dept:
        employees = employees.filter(job_title=selected_dept)
    if selected_status:
        employees = employees.filter(status=selected_status)

    if search_query:
        if len(search_query) == 1:
            # If user enters 1 character: search first name that starts with it
            employees = employees.filter(first_name__istartswith=search_query)
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )


    employees = employees.order_by('last_name', 'first_name')
    total_search_results = employees.count()

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'on_leave_employees': on_leave_employees,
        'employees': employees,
        'departments': departments,
        "total_search_results": total_search_results,

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


