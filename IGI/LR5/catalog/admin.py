from django.contrib import admin
from django.utils.html import format_html
from .models import FurnitureCategory, FurnitureModel, FurnitureItem, Tag, Promo


@admin.register(FurnitureCategory)
class FurnitureCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'item_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Кол-во изделий'


@admin.register(FurnitureModel)
class FurnitureModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


class TagInline(admin.TabularInline):
    model = FurnitureItem.tags.through
    extra = 1


@admin.register(FurnitureItem)
class FurnitureItemAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name', 'category', 'model', 'price', 'is_active', 'thumbnail']
    list_filter = ['category', 'model', 'is_active']
    search_fields = ['name', 'product_code', 'description']
    list_editable = ['price', 'is_active']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основное', {'fields': ('product_code', 'name', 'category', 'model', 'is_active')}),
        ('Цена и характеристики', {'fields': ('price', 'weight', 'dimensions', 'material')}),
        ('Описание и медиа', {'fields': ('description', 'image', 'tags')}),
        ('Системные', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="40" style="object-fit:cover"/>', obj.image.url)
        return '—'
    thumbnail.short_description = 'Фото'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_to', 'used_count']
    list_filter = ['is_active', 'discount_type']
    search_fields = ['code', 'description']
    list_editable = ['is_active']
    filter_horizontal = ['applicable_categories']
