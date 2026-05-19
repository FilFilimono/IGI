from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['subtotal']

    def subtotal(self, obj):
        return f'{obj.subtotal:.2f} руб.' if obj.pk else '—'
    subtotal.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'client', 'status', 'order_date', 'due_date', 'total_display', 'manager']
    list_filter = ['status', 'order_date', 'manager']
    search_fields = ['order_number', 'client__company_name']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_date', 'created_at', 'updated_at', 'total_display']
    date_hierarchy = 'order_date'

    def total_display(self, obj):
        return f'{obj.total_amount:.2f} руб.'
    total_display.short_description = 'Сумма заказа'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'furniture', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['furniture__category']
    search_fields = ['order__order_number', 'furniture__name']
