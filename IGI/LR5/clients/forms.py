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
            age = (date.today() - bd).days // 365
            if age < settings.MIN_AGE:
                raise forms.ValidationError(f'Контактному лицу должно быть не менее {settings.MIN_AGE} лет.')
        return bd
