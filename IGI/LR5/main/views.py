import logging
import requests
import calendar
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db.models import Avg
from .models import Article, GlossaryTerm, Review, Vacancy, CompanyInfo
from .forms import ReviewForm

logger = logging.getLogger('catalog')


def home(request):
    latest_article = Article.objects.filter(is_published=True).first()
    avg_rating = Review.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
    reviews_count = Review.objects.filter(is_approved=True).count()

    # Weather API (OpenWeatherMap)
    weather = None
    if settings.OPENWEATHER_API_KEY:
        try:
            city = 'Minsk'
            resp = requests.get(
                'https://api.openweathermap.org/data/2.5/weather',
                params={'q': city, 'appid': settings.OPENWEATHER_API_KEY, 'units': 'metric', 'lang': 'ru'},
                timeout=3
            )
            if resp.status_code == 200:
                data = resp.json()
                weather = {
                    'city': city,
                    'temp': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                }
        except Exception as e:
            logger.warning(f'Weather API error: {e}')

    # Currency API (exchangerate)
    currency = None
    try:
        resp = requests.get(
            'https://open.er-api.com/v6/latest/USD',
            timeout=3
        )
        if resp.status_code == 200:
            data = resp.json()
            currency = {
                'USD_BYN': round(data['rates'].get('BYN', 0), 4),
                'EUR_BYN': round(data['rates'].get('BYN', 0) / data['rates'].get('EUR', 1), 4),
            }
    except Exception as e:
        logger.warning(f'Currency API error: {e}')

    context = {
        'latest_article': latest_article,
        'avg_rating': avg_rating,
        'reviews_count': reviews_count,
        'weather': weather,
        'currency': currency,
    }
    return render(request, 'main/home.html', context)


def about(request):
    info = CompanyInfo.objects.first()
    return render(request, 'main/about.html', {'info': info})


def news(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'main/news.html', {'articles': articles})


def glossary(request):
    terms = GlossaryTerm.objects.all().order_by('question')
    q = request.GET.get('q', '')
    if q:
        terms = terms.filter(question__icontains=q) | terms.filter(answer__icontains=q)
    return render(request, 'main/glossary.html', {'terms': terms, 'q': q})


def contacts(request):
    from employees.models import Employee
    employees = Employee.objects.filter(is_active=True).select_related('department')
    return render(request, 'main/contacts.html', {'employees': employees})


def privacy(request):
    return render(request, 'main/privacy.html')


def vacancies(request):
    vacancies_list = Vacancy.objects.filter(is_active=True)
    return render(request, 'main/vacancies.html', {'vacancies': vacancies_list})


def reviews(request):
    reviews_list = Review.objects.filter(is_approved=True).order_by('-created_at')
    form = None
    if request.user.is_authenticated:
        form = ReviewForm()
    avg_rating = reviews_list.aggregate(avg=Avg('rating'))['avg']
    return render(request, 'main/reviews.html', {
        'reviews': reviews_list,
        'form': form,
        'avg_rating': avg_rating,
    })


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.name = request.user.get_full_name() or request.user.username
            review.save()
            messages.success(request, 'Ваш отзыв отправлен на проверку.')
            logger.info(f'New review from user {request.user.username}')
        else:
            messages.error(request, 'Ошибка при отправке отзыва.')
    return redirect('main:reviews')
