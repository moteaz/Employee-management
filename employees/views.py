from django.shortcuts import render ,redirect,get_object_or_404
from .models import Employee
from .forms import EmployeeForm

# Create your views here.

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

def add_employee(request):
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


def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('home')

    return render(request, 'employees/deleteAlert.html', {'employee': employee})


def profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/profileEmployee.html', {'employee': employee})

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'employees/updateEmployee.html', {'form': form, 'employee': employee})


