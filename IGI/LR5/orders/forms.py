from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'client', 'due_date', 'status', 'promo', 'notes', 'manager']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=['furniture', 'quantity', 'unit_price'],
    extra=1, can_delete=True
)
