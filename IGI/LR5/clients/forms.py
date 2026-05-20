from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_code', 'company_name', 'phone', 'city', 'address', 'email',
                  'contact_person', 'birth_date', 'is_active']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX'}),
        }

    def clean_birth_date(self):
        from datetime import date
        bd = self.cleaned_data.get('birth_date')
        if bd:
            from django.conf import settings
            today = date.today()
            if bd > today:
                raise forms.ValidationError('Дата рождения не может быть в будущем.')
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            if age < settings.MIN_AGE:
                raise forms.ValidationError(f'Контактному лицу должно быть не менее {settings.MIN_AGE} лет.')
        return bd
