import pytz
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, label='Роль')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Логин', 'first_name': 'Имя',
            'last_name': 'Фамилия', 'email': 'Email',
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        validate_password(pwd)
        return pwd

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['timezone', 'avatar']
        widgets = {'timezone': forms.Select(choices=TIMEZONE_CHOICES)}
