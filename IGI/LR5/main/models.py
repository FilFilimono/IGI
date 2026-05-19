from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    """Новости / статьи"""
    title = models.CharField(_('Заголовок'), max_length=200)
    summary = models.CharField(_('Краткое содержание'), max_length=500)
    content = models.TextField(_('Содержание'))
    image = models.ImageField(_('Изображение'), upload_to='articles/', blank=True, null=True)
    is_published = models.BooleanField(_('Опубликована'), default=False)
    published_at = models.DateTimeField(_('Дата публикации'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class GlossaryTerm(models.Model):
    """Словарь терминов — FAQ"""
    question = models.CharField(_('Вопрос'), max_length=300)
    answer = models.TextField(_('Ответ'))
    added_at = models.DateField(_('Дата добавления'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Термин / FAQ')
        verbose_name_plural = _('Словарь терминов / FAQ')
        ordering = ['question']

    def __str__(self):
        return self.question


class Review(models.Model):
    """Отзывы"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    # ForeignKey: отзыв принадлежит пользователю
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Пользователь')
    )
    name = models.CharField(_('Имя'), max_length=100)
    rating = models.PositiveSmallIntegerField(_('Оценка'), choices=RATING_CHOICES)
    text = models.TextField(_('Текст отзыва'))
    is_approved = models.BooleanField(_('Одобрен'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.name} ({self.rating}★)'


class Vacancy(models.Model):
    """Вакансии"""
    title = models.CharField(_('Название вакансии'), max_length=200)
    description = models.TextField(_('Описание'))
    requirements = models.TextField(_('Требования'), blank=True)
    salary_from = models.DecimalField(_('Зарплата от'), max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField(_('Зарплата до'), max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    """О компании (синглтон)"""
    title = models.CharField(_('Заголовок'), max_length=200, default='О нас')
    content = models.TextField(_('Содержание'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Информация о компании')
        verbose_name_plural = _('Информация о компании')

    def __str__(self):
        return self.title
