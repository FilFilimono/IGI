import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Client
from .forms import ClientForm

logger = logging.getLogger('clients')


@login_required
def client_list(request):
    clients = Client.objects.all()
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')

    q = request.GET.get('q', '')
    city = request.GET.get('city', '')
    sort = request.GET.get('sort', 'company_name')
    if q:
        clients = clients.filter(
            Q(company_name__icontains=q) | Q(client_code__icontains=q) | Q(phone__icontains=q)
        )
    if city:
        clients = clients.filter(city=city)
    clients = clients.order_by(sort)

    city_choices = Client.CITY_CHOICES
    return render(request, 'clients/client_list.html', {
        'clients': clients, 'q': q, 'city': city, 'sort': sort, 'city_choices': city_choices
    })


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not request.user.is_staff:
        try:
            if request.user.client_profile != client:
                messages.error(request, 'Нет доступа.')
                return redirect('main:home')
        except Exception:
            messages.error(request, 'Нет доступа.')
            return redirect('main:home')
    return render(request, 'clients/client_detail.html', {'client': client})


@login_required
def client_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')
    form = ClientForm(request.POST or None)
    if form.is_valid():
        client = form.save()
        logger.info(f'Client created: {client.client_code}')
        messages.success(request, f'Клиент «{client.company_name}» создан.')
        return redirect('clients:client_detail', pk=client.pk)
    return render(request, 'clients/client_form.html', {'form': form, 'action': 'Создать'})


@login_required
def client_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        messages.success(request, f'Клиент «{client.company_name}» обновлён.')
        return redirect('clients:client_detail', pk=pk)
    return render(request, 'clients/client_form.html', {'form': form, 'action': 'Сохранить', 'client': client})


@login_required
def client_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Нет доступа.')
        return redirect('main:home')
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        name = client.company_name
        client.delete()
        messages.success(request, f'Клиент «{name}» удалён.')
        return redirect('clients:client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})
