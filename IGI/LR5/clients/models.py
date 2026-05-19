import logging
import re
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

logger = logging.getLogger('clients')

PHONE_VALIDATOR = RegexValidator(
    regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
    message='Формат: +375 (29) XXX-XX-XX'
)


class Client(models.Model):
    """Оптовый покупатель / компания-заказчик"""
    CITY_CHOICES = [
        ('minsk', 'Минск'), ('gomel', 'Гомель'), ('mogilev', 'Могилев'),
        ('vitebsk', 'Витебск'), ('grodno', 'Гродно'), ('brest', 'Брест'),
        ('other', 'Другой'),
    ]
    # OneToOneField: клиент привязан к одному пользователю системы
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='client_profile',
        verbose_name=_('Пользователь')
    )
    client_code = models.CharField(_('Код клиента'), max_length=20, unique=True)
    company_name = models.CharField(_('Название компании'), max_length=200)
    phone = models.CharField(_('Телефон'), max_length=20, validators=[PHONE_VALIDATOR])
    city = models.CharField(_('Город'), max_length=50, choices=CITY_CHOICES, default='minsk')
    address = models.CharField(_('Адрес'), max_length=300)
    email = models.EmailField(_('Email'), blank=True)
    contact_person = models.CharField(_('Контактное лицо'), max_length=200, blank=True)
    birth_date = models.DateField(_('Дата рождения контактного лица'), null=True, blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')
        ordering = ['company_name']

    def __str__(self):
        return f'{self.company_name} ({self.client_code})'

    def save(self, *args, **kwargs):
        logger.info(f'Saving Client: {self.client_code} - {self.company_name}')
        super().save(*args, **kwargs)

    @property
    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
