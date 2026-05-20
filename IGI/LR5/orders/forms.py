from datetime import date, timedelta
from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'client', 'due_date', 'status', 'promo', 'notes', 'manager']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class BuyerOrderForm(forms.ModelForm):
    """Заказ от покупателя: клиент и номер подставляются автоматически."""
    class Meta:
        model = Order
        fields = ['due_date', 'promo', 'notes']
        labels = {
            'due_date': 'Желаемая дата выполнения',
            'promo': 'Промокод',
            'notes': 'Примечания',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_due_date(self):
        due = self.cleaned_data.get('due_date')
        if due and due < date.today():
            raise forms.ValidationError('Дата выполнения не может быть в прошлом.')
        return due


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=['furniture', 'quantity', 'unit_price'],
    extra=1, can_delete=True
)

BuyerOrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=['furniture', 'quantity'],
    extra=1,
    can_delete=False,
    max_num=10,
    min_num=1,
    validate_min=True,
)
