from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    """Профиль пользователя"""
    ROLE_CHOICES = [
        ('buyer', 'Покупатель'),
        ('employee', 'Сотрудник'),
    ]
    # OneToOneField: один профиль — один пользователь
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('Пользователь'))
    role = models.CharField(_('Роль'), max_length=20, choices=ROLE_CHOICES, default='buyer')
    timezone = models.CharField(_('Часовой пояс'), max_length=50, default='Europe/Minsk')
    avatar = models.ImageField(_('Аватар'), upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')

    def __str__(self):
        return f'Профиль {self.user.username} ({self.get_role_display()})'

    @property
    def is_employee(self):
        return self.role == 'employee'

    @property
    def is_buyer(self):
        return self.role == 'buyer'
