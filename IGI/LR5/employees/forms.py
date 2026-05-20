from django import forms
from datetime import date
from django.conf import settings
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'middle_name', 'position', 'department',
                  'phone', 'email', 'birth_date', 'hire_date', 'photo', 'description',
                  'is_active', 'managed_clients']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'managed_clients': forms.CheckboxSelectMultiple(),
        }

    def clean_birth_date(self):
        bd = self.cleaned_data.get('birth_date')
        if bd:
            today = date.today()
            if bd > today:
                raise forms.ValidationError('Дата рождения не может быть в будущем.')
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            if age < settings.MIN_AGE:
                raise forms.ValidationError(f'Сотрудник должен быть не моложе {settings.MIN_AGE} лет.')
        return bd
