import logging
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('catalog')


class FurnitureCategory(models.Model):
    name = models.CharField(_('Название'), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Вид мебели')
        verbose_name_plural = _('Виды мебели')
        ordering = ['name']

    def __str__(self):
        return self.name


class FurnitureModel(models.Model):

    name = models.CharField(_('Название модели'), max_length=100)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Модель')
        verbose_name_plural = _('Модели')
        ordering = ['name']

    def __str__(self):
        return self.name


class FurnitureItem(models.Model):
    
    
    product_code = models.CharField(_('Код продукта'), max_length=50, unique=True)
    name = models.CharField(_('Название'), max_length=200)
    
    category = models.ForeignKey(
        FurnitureCategory,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name=_('Вид мебели')
    )
    
    model = models.ForeignKey(
        FurnitureModel,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name=_('Модель')
    )
    price = models.DecimalField(
        _('Цена (руб.)'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(_('Производится'), default=True)
    image = models.ImageField(_('Изображение'), upload_to='furniture/', blank=True, null=True)
    description = models.TextField(_('Описание'), blank=True)
    weight = models.DecimalField(_('Вес (кг)'), max_digits=8, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(_('Габариты (ДxШxВ см)'), max_length=100, blank=True)
    material = models.CharField(_('Материал'), max_length=200, blank=True)
    
    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('Теги'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Изделие')
        verbose_name_plural = _('Изделия')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.product_code})'

    def save(self, *args, **kwargs):
        logger.info(f'Saving FurnitureItem: {self.product_code} - {self.name}')
        super().save(*args, **kwargs)


class Tag(models.Model):
    
    name = models.CharField(_('Тег'), max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name


class Promo(models.Model):
    
    DISCOUNT_TYPE_CHOICES = [
        ('percent', _('Процент')),
        ('fixed', _('Фиксированная сумма')),
    ]
    code = models.CharField(_('Код'), max_length=50, unique=True)
    discount_type = models.CharField(_('Тип скидки'), max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    discount_value = models.DecimalField(_('Размер скидки'), max_digits=10, decimal_places=2)
    description = models.TextField(_('Описание'), blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    valid_from = models.DateTimeField(_('Действует с'))
    valid_to = models.DateTimeField(_('Действует до'))
    usage_limit = models.PositiveIntegerField(_('Лимит использований'), default=100)
    used_count = models.PositiveIntegerField(_('Использован раз'), default=0)
    
    applicable_categories = models.ManyToManyField(
        FurnitureCategory, blank=True, verbose_name=_('Применимо к категориям')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Промокод')
        verbose_name_plural = _('Промокоды')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} ({self.discount_value}{"%" if self.discount_type == "percent" else " руб."})'

    @property
    def is_archived(self):
        from django.utils import timezone
        return not self.is_active or self.valid_to < timezone.now()
