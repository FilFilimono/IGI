from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_code', 'company_name', 'city', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['city', 'is_active']
    search_fields = ['company_name', 'client_code', 'phone', 'email', 'contact_person']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основное', {'fields': ('client_code', 'company_name', 'user', 'is_active')}),
        ('Контакты', {'fields': ('phone', 'email', 'city', 'address', 'contact_person', 'birth_date')}),
        ('Системные', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
