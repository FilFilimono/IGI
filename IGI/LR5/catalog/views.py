import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum
from .models import FurnitureItem, FurnitureCategory, Promo
from .forms import FurnitureItemForm, FurnitureFilterForm

logger = logging.getLogger('catalog')


def item_list(request):
    items = FurnitureItem.objects.select_related('category', 'model').prefetch_related('tags')
    form = FurnitureFilterForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        is_active = form.cleaned_data.get('is_active')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        sort = form.cleaned_data.get('sort')

        if q:
            items = items.filter(
                Q(name__icontains=q) | Q(product_code__icontains=q) | Q(description__icontains=q)
            )
        if category:
            items = items.filter(category=category)
        if is_active is not None:
            items = items.filter(is_active=is_active)
        if price_min is not None:
            items = items.filter(price__gte=price_min)
        if price_max is not None:
            items = items.filter(price__lte=price_max)
        if sort:
            items = items.order_by(sort)

    categories = FurnitureCategory.objects.annotate(cnt=Count('items')).filter(cnt__gt=0)
    return render(request, 'catalog/item_list.html', {
        'items': items,
        'form': form,
        'categories': categories,
    })


def item_detail(request, pk):
    item = get_object_or_404(FurnitureItem, pk=pk)
    related = FurnitureItem.objects.filter(category=item.category).exclude(pk=pk)[:4]
    logger.debug(f'Viewing item {pk}: {item.name}')
    return render(request, 'catalog/item_detail.html', {'item': item, 'related': related})


@login_required
def item_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('catalog:item_list')
    form = FurnitureItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        item = form.save()
        logger.info(f'Created item {item.pk}: {item.name} by {request.user.username}')
        messages.success(request, f'Изделие «{item.name}» создано.')
        return redirect('catalog:item_detail', pk=item.pk)
    return render(request, 'catalog/item_form.html', {'form': form, 'action': 'Создать'})


@login_required
def item_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('catalog:item_list')
    item = get_object_or_404(FurnitureItem, pk=pk)
    form = FurnitureItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f'Updated item {pk} by {request.user.username}')
        messages.success(request, f'Изделие «{item.name}» обновлено.')
        return redirect('catalog:item_detail', pk=pk)
    return render(request, 'catalog/item_form.html', {'form': form, 'action': 'Сохранить', 'item': item})


@login_required
def item_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Нет доступа.')
        return redirect('catalog:item_list')
    item = get_object_or_404(FurnitureItem, pk=pk)
    if request.method == 'POST':
        name = item.name
        item.delete()
        logger.info(f'Deleted item {pk} ({name}) by {request.user.username}')
        messages.success(request, f'Изделие «{name}» удалено.')
        return redirect('catalog:item_list')
    return render(request, 'catalog/item_confirm_delete.html', {'item': item})


def promo_list(request):
    active_promos = Promo.objects.filter(is_active=True)
    archived_promos = Promo.objects.filter(is_active=False)
    from django.utils import timezone
    now = timezone.now()
    expired = Promo.objects.filter(is_active=True, valid_to__lt=now)
    return render(request, 'catalog/promo_list.html', {
        'active_promos': active_promos.filter(valid_to__gte=now),
        'archived_promos': list(archived_promos) + list(expired),
    })


def category_list(request):
    categories = FurnitureCategory.objects.annotate(
        item_count=Count('items'),
        avg_price=Avg('items__price'),
    )
    return render(request, 'catalog/category_list.html', {'categories': categories})
