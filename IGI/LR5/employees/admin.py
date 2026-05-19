from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_count']

    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Сотрудников'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'department', 'phone', 'email', 'is_active', 'photo_thumb']
    list_filter = ['position', 'department', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['is_active']
    filter_horizontal = ['managed_clients']
    readonly_fields = ['created_at', 'updated_at']

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;object-fit:cover"/>', obj.photo.url)
        return '—'
    photo_thumb.short_description = 'Фото'
