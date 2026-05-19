import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg
from django.db.models.functions import TruncMonth, TruncYear
from .models import Order, OrderItem
from .forms import OrderForm

logger = logging.getLogger('orders')


@login_required
def order_list(request):
    orders = Order.objects.select_related('client', 'manager').prefetch_related('items')
    if not request.user.is_staff:
        try:
            client = request.user.client_profile
            orders = orders.filter(client=client)
        except Exception:
            try:
                emp = request.user.employee_profile
                orders = orders.filter(manager=emp)
            except Exception:
                orders = orders.none()

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    sort = request.GET.get('sort', '-order_date')
    if q:
        orders = orders.filter(Q(order_number__icontains=q) | Q(client__company_name__icontains=q))
    if status:
        orders = orders.filter(status=status)
    orders = orders.order_by(sort)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'q': q, 'status': status, 'sort': sort,
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_staff:
        try:
            client = request.user.client_profile
            if order.client != client:
                messages.error(request, 'Нет доступа.')
                return redirect('orders:order_list')
        except Exception:
            pass
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('orders:order_list')
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        logger.info(f'Order {order.order_number} created by {request.user.username}')
        messages.success(request, f'Заказ {order.order_number} создан.')
        return redirect('orders:order_detail', pk=order.pk)
    return render(request, 'orders/order_form.html', {'form': form, 'action': 'Создать'})


@login_required
def order_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('orders:order_list')
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, f'Заказ {order.order_number} обновлён.')
        return redirect('orders:order_detail', pk=pk)
    return render(request, 'orders/order_form.html', {'form': form, 'action': 'Сохранить', 'order': order})


@login_required
def order_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Нет доступа.')
        return redirect('orders:order_list')
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        num = order.order_number
        order.delete()
        messages.success(request, f'Заказ {num} удалён.')
        return redirect('orders:order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})


@login_required
def statistics(request):
    if not request.user.is_superuser:
        messages.error(request, 'Нет доступа.')
        return redirect('orders:order_list')

    # Ежемесячный объем продаж
    monthly_qs = (
        Order.objects.filter(status='delivered')
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total=Sum('items__unit_price'))
        .order_by('month')
    )
    monthly_json = json.dumps({
        'labels': [str(m['month'].strftime('%m/%Y')) if m['month'] else '' for m in monthly_qs],
        'values': [float(m['total'] or 0) for m in monthly_qs],
    })

    # Популярность мебели
    popular = (
        OrderItem.objects.values('furniture__name', 'furniture__category__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:10]
    )

    # Прибыль по категориям
    by_category = (
        OrderItem.objects.values('furniture__category__name')
        .annotate(total_revenue=Sum('unit_price'), total_qty=Sum('quantity'))
        .order_by('-total_revenue')
    )
    category_json = json.dumps({
        'labels': [c['furniture__category__name'] or 'Без категории' for c in by_category],
        'values': [float(c['total_revenue'] or 0) for c in by_category],
    })

    # Клиенты по городам
    from clients.models import Client
    clients_by_city = (
        Client.objects.values('city')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    city_json = json.dumps({
        'labels': [c['city'] for c in clients_by_city],
        'values': [c['count'] for c in clients_by_city],
    })

    # Статистика продаж
    revenues = list(
        Order.objects.filter(status='delivered')
        .annotate(rev=Sum('items__unit_price'))
        .values_list('rev', flat=True)
    )
    revenues = [float(r) for r in revenues if r is not None]
    stats_data = {}
    if revenues:
        srt = sorted(revenues)
        n = len(srt)
        stats_data = {
            'mean': round(sum(srt) / n, 2),
            'median': round(srt[n // 2], 2),
            'total': round(sum(srt), 2),
            'count': n,
        }

    # Годовой отчет
    yearly = (
        Order.objects.filter(status='delivered')
        .annotate(year=TruncYear('order_date'))
        .values('year')
        .annotate(total=Sum('items__unit_price'), count=Count('id'))
        .order_by('year')
    )

    # Линейный тренд продаж (прогноз)
    trend_json = json.dumps({'labels': [], 'values': [], 'trend': []})
    if len(revenues) >= 2:
        import statistics as st
        x = list(range(len(revenues)))
        x_mean = sum(x) / len(x)
        y_mean = sum(revenues) / len(revenues)
        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, revenues))
        denominator = sum((xi - x_mean) ** 2 for xi in x) or 1
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        trend = [round(intercept + slope * xi, 2) for xi in x]
        # Прогноз на 3 периода вперед
        for i in range(1, 4):
            xi = len(revenues) + i - 1
            trend.append(round(intercept + slope * xi, 2))
        trend_json = json.dumps({
            'labels': [f'Период {i+1}' for i in range(len(revenues))] + ['Прогноз+1', 'Прогноз+2', 'Прогноз+3'],
            'values': revenues + [None, None, None],
            'trend': trend,
        })

    return render(request, 'orders/statistics.html', {
        'monthly': monthly_qs,
        'monthly_json': monthly_json,
        'popular': popular,
        'by_category': by_category,
        'category_json': category_json,
        'clients_by_city': clients_by_city,
        'city_json': city_json,
        'stats_data': stats_data,
        'yearly': yearly,
        'trend_json': trend_json,
    })
