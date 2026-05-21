import logging
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('employees')

PHONE_VALIDATOR = RegexValidator(
    regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
    message='Формат: +375 (29) XXX-XX-XX'
)


class Department(models.Model):
    name = models.CharField(_('Название'), max_length=100, unique=True)
    description = models.TextField(_('Описание'), blank=True)

    class Meta:
        verbose_name = _('Отдел')
        verbose_name_plural = _('Отделы')

    def __str__(self):
        return self.name


class Employee(models.Model):
   
    POSITION_CHOICES = [
        ('director', 'Директор'), ('manager', 'Менеджер'),
        ('designer', 'Дизайнер'), ('craftsman', 'Мастер'),
        ('accountant', 'Бухгалтер'), ('logist', 'Логист'), ('other', 'Другое'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='employee_profile',
        verbose_name=_('Пользователь')
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='employees',
        verbose_name=_('Отдел')
    )
    first_name = models.CharField(_('Имя'), max_length=100)
    last_name = models.CharField(_('Фамилия'), max_length=100)
    middle_name = models.CharField(_('Отчество'), max_length=100, blank=True)
    position = models.CharField(_('Должность'), max_length=50, choices=POSITION_CHOICES)
    phone = models.CharField(_('Телефон'), max_length=20, validators=[PHONE_VALIDATOR])
    email = models.EmailField(_('Email'))
    birth_date = models.DateField(_('Дата рождения'))
    hire_date = models.DateField(_('Дата найма'))
    photo = models.ImageField(_('Фото'), upload_to='employees/', blank=True, null=True)
    description = models.TextField(_('Описание обязанностей'), blank=True)
    is_active = models.BooleanField(_('Работает'), default=True)
    
    managed_clients = models.ManyToManyField(
        'clients.Client',
        blank=True,
        related_name='managers',
        verbose_name=_('Закреплённые клиенты')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} — {self.get_position_display()}'

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
