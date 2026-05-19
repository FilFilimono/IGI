import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import UserProfile

logger = logging.getLogger('accounts')


def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        role = form.cleaned_data.get('role', 'buyer')
        UserProfile.objects.get_or_create(user=user, defaults={"role": role})
        login(request, user)
        logger.info(f'New user registered: {user.username}')
        messages.success(request, f'Добро пожаловать, {user.username}!')
        return redirect('main:home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logger.info(f'User logged in: {username}')
            next_url = request.GET.get('next', 'main:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        logger.info(f'User logged out: {username}')
        messages.info(request, 'Вы вышли из системы.')
    return redirect('main:home')


@login_required
def profile(request):
    try:
        prof = request.user.profile
    except UserProfile.DoesNotExist:
        prof = UserProfile.objects.create(user=request.user)

    form = ProfileForm(request.POST or None, request.FILES or None, instance=prof)
    if form.is_valid():
        form.save()
        tz = form.cleaned_data.get('timezone')
        if tz:
            request.session['django_timezone'] = tz
        messages.success(request, 'Профиль обновлён.')
        return redirect('accounts:profile')

    orders = []
    client = None
    try:
        client = request.user.client_profile
        orders = client.orders.all().order_by('-order_date')[:5]
    except Exception:
        pass

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': prof,
        'client': client,
        'orders': orders,
    })
