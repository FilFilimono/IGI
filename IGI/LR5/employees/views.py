import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Employee, Department
from .forms import EmployeeForm

logger = logging.getLogger('clients')


def employee_list(request):
    employees = Employee.objects.filter(is_active=True).select_related('department')
    return render(request, 'employees/employee_list.html', {'employees': employees})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
def employee_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        emp = form.save()
        messages.success(request, f'Сотрудник «{emp.full_name}» добавлен.')
        return redirect('employees:employee_detail', pk=emp.pk)
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'Добавить'})


@login_required
def employee_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')
    emp = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=emp)
    if form.is_valid():
        form.save()
        messages.success(request, f'Данные сотрудника обновлены.')
        return redirect('employees:employee_detail', pk=pk)
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'Сохранить', 'emp': emp})


@login_required
def employee_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.is_active = False
        emp.save()
        messages.success(request, f'Сотрудник деактивирован.')
        return redirect('employees:employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'emp': emp})
