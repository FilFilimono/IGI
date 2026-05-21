import logging
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from catalog.models import FurnitureItem, Promo
from clients.models import Client

logger = logging.getLogger('orders')


class Order(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает'), ('confirmed', 'Подтверждён'),
        ('in_production', 'В производстве'), ('ready', 'Готов'),
        ('delivered', 'Доставлен'), ('cancelled', 'Отменён'),
    ]
    order_number = models.CharField(_('Номер заказа'), max_length=30, unique=True)
    
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Клиент')
    )
    order_date = models.DateTimeField(_('Дата заказа'), auto_now_add=True)
    due_date = models.DateField(_('Дата выполнения'))
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='pending')
    promo = models.ForeignKey(
        Promo,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders',
        verbose_name=_('Промокод')
    )
    notes = models.TextField(_('Примечания'), blank=True)

    manager = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='managed_orders',
        verbose_name=_('Менеджер')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['-order_date']

    def __str__(self):
        return f'Заказ {self.order_number} — {self.client.company_name}'

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_after_discount(self):
        total = self.total_amount
        if self.promo and not self.promo.is_archived:
            if self.promo.discount_type == 'percent':
                total = total * (1 - self.promo.discount_value / 100)
            else:
                total = max(0, total - self.promo.discount_value)
        return total

    def save(self, *args, **kwargs):
        logger.info(f'Saving Order: {self.order_number}')
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Заказ'))
    
    furniture = models.ForeignKey(
        FurnitureItem,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('Изделие')
    )
    quantity = models.PositiveIntegerField(_('Количество'), validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(_('Цена за единицу'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Позиция заказа')
        verbose_name_plural = _('Позиции заказа')
        unique_together = ['order', 'furniture']

    def __str__(self):
        return f'{self.furniture.name} x{self.quantity}'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.furniture.price
        super().save(*args, **kwargs)
