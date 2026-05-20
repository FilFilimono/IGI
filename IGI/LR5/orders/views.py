import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from catalog.models import FurnitureItem
from .models import Order, OrderItem
from .forms import OrderForm, BuyerOrderForm, OrderItemFormSet, BuyerOrderItemFormSet
from .charts import monthly_trend_chart, city_bar_chart

logger = logging.getLogger('orders')

_ORDER_ITEM_SUBTOTAL = ExpressionWrapper(
    F('items__unit_price') * F('items__quantity'),
    output_field=DecimalField(max_digits=12, decimal_places=2),
)
_ITEM_SUBTOTAL = ExpressionWrapper(
    F('unit_price') * F('quantity'),
    output_field=DecimalField(max_digits=12, decimal_places=2),
)


def _linear_trend(values, forecast=0):
    if not values:
        return []
    if len(values) == 1:
        return [round(values[0], 2)]

    x = list(range(len(values)))
    x_mean = sum(x) / len(x)
    y_mean = sum(values) / len(values)
    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, values))
    denominator = sum((xi - x_mean) ** 2 for xi in x) or 1
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    trend = [round(intercept + slope * xi, 2) for xi in x]
    for i in range(1, forecast + 1):
        trend.append(round(intercept + slope * (len(values) + i - 1), 2))
    return trend


def _get_client_profile(user):
    try:
        return user.client_profile
    except Exception:
        return None


def _generate_order_number():
    year = timezone.now().year
    prefix = f'ORD-{year}-'
    last = (
        Order.objects.filter(order_number__startswith=prefix)
        .order_by('-order_number')
        .first()
    )
    if last:
        try:
            num = int(last.order_number.split('-')[-1]) + 1
        except ValueError:
            num = 1
    else:
        num = 1
    return f'{prefix}{num:03d}'


@login_required
def order_list(request):
    orders = Order.objects.select_related('client', 'manager').prefetch_related('items')
    if not request.user.is_staff:
        client = _get_client_profile(request.user)
        if client:
            orders = orders.filter(client=client)
        else:
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
        'can_create': request.user.is_staff or _get_client_profile(request.user),
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_staff:
        client = _get_client_profile(request.user)
        if client and order.client != client:
            messages.error(request, 'Нет доступа.')
            return redirect('orders:order_list')
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_create(request):
    client_profile = _get_client_profile(request.user)
    is_buyer = client_profile and not request.user.is_staff

    if not request.user.is_staff and not is_buyer:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')

    if is_buyer:
        form = BuyerOrderForm(request.POST or None)
        formset = BuyerOrderItemFormSet(request.POST or None)
        active_items = FurnitureItem.objects.filter(is_active=True)
        for f in formset.forms:
            f.fields['furniture'].queryset = active_items
        if request.method == 'POST':
            if form.is_valid() and formset.is_valid():
                order = form.save(commit=False)
                order.order_number = _generate_order_number()
                order.client = client_profile
                order.status = 'pending'
                order.manager = None
                order.save()
                formset.instance = order
                formset.save()
                if not order.items.exists():
                    order.delete()
                    messages.error(request, 'Добавьте хотя бы одно изделие в заказ.')
                else:
                    logger.info(f'Order {order.order_number} created by buyer {request.user.username}')
                    messages.success(request, f'Заказ {order.order_number} отправлен.')
                    return redirect('orders:order_detail', pk=order.pk)
        return render(request, 'orders/order_form.html', {
            'form': form,
            'formset': formset,
            'action': 'Оформить',
            'is_buyer': True,
        })

    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        logger.info(f'Order {order.order_number} created by {request.user.username}')
        messages.success(request, f'Заказ {order.order_number} создан.')
        return redirect('orders:order_detail', pk=order.pk)
    return render(request, 'orders/order_form.html', {
        'form': form,
        'action': 'Создать',
        'is_buyer': False,
    })


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
    return render(request, 'orders/order_form.html', {'form': form, 'action': 'Сохранить', 'order': order, 'is_buyer': False})


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

    monthly_qs = (
        Order.objects.filter(status='delivered')
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total=Sum(_ORDER_ITEM_SUBTOTAL))
        .order_by('month')
    )
    monthly_labels = [m['month'].strftime('%m/%Y') if m['month'] else '' for m in monthly_qs]
    monthly_values = [float(m['total'] or 0) for m in monthly_qs]

    forecast_periods = 3
    chart_labels = monthly_labels[:]
    chart_values = monthly_values[:]
    trend_values = _linear_trend(monthly_values, forecast=forecast_periods)
    if len(monthly_values) >= 2:
        chart_labels += [f'Прогноз+{i}' for i in range(1, forecast_periods + 1)]
        chart_values += [None] * forecast_periods

    popular = (
        OrderItem.objects.filter(order__status='delivered')
        .values('furniture__name', 'furniture__category__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:10]
    )

    by_category = (
        OrderItem.objects.filter(order__status='delivered')
        .values('furniture__category__name')
        .annotate(total_revenue=Sum(_ITEM_SUBTOTAL), total_qty=Sum('quantity'))
        .order_by('-total_revenue')
    )

    from clients.models import Client
    clients_by_city = (
        Client.objects.values('city')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    city_labels = [c['city'] for c in clients_by_city]
    city_values = [c['count'] for c in clients_by_city]

    revenues = [
        float(r) for r in Order.objects.filter(status='delivered')
        .annotate(rev=Sum(_ORDER_ITEM_SUBTOTAL))
        .values_list('rev', flat=True)
        if r is not None
    ]
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

    yearly = (
        Order.objects.filter(status='delivered')
        .annotate(year=TruncYear('order_date'))
        .values('year')
        .annotate(total=Sum(_ORDER_ITEM_SUBTOTAL), count=Count('pk', distinct=True))
        .order_by('year')
    )

    return render(request, 'orders/statistics.html', {
        'popular': popular,
        'by_category': by_category,
        'stats_data': stats_data,
        'yearly': yearly,
        'chart_trend': monthly_trend_chart(chart_labels, chart_values, trend_values),
        'chart_city': city_bar_chart(city_labels, city_values),
    })
