# 🪑 МебельФабрика — Django Web Application

Веб-сайт мебельной фабрики на Django 6 с полным функционалом управления заказами, каталогом, клиентами и аналитикой.

## 🚀 Быстрый старт

### Локально (SQLite)
```bash
git clone <repo>
cd <каталог_с_manage.py>        # корень проекта, например IGI/LR5
python3 -m venv furniture_factory_project
source furniture_factory_project/bin/activate   # Windows: furniture_factory_project\Scripts\activate
pip install -r requirements.txt
mkdir -p static                 # убирает предупреждение staticfiles.W004
python manage.py migrate
python manage.py seed_data      # тестовые данные (после migrate)
python manage.py runserver
```

Если раньше запускали `seed_data` без миграций и база «сломана», удалите файл `db.sqlite3` и снова выполните `migrate`, затем `seed_data`.

**Доступ:** http://127.0.0.1:8000  
**Логины:** `admin / admin123` · `manager1 / manager123` · `buyer1 / buyer123`

### Docker Compose (PostgreSQL)
```bash
docker-compose up --build
```
Сайт доступен на http://localhost

## 🧪 Тесты
```bash
python manage.py test tests --verbosity=2      # Django test runner
python -m coverage run manage.py test tests    # с покрытием
python -m coverage report                      # отчёт (86%+)
```

## 📁 Структура проекта
```
furniture_factory/       # настройки, urls, middleware
main/                    # главная, новости, отзывы, FAQ, вакансии
catalog/                 # каталог мебели, категории, промокоды
orders/                  # заказы, статистика, аналитика
clients/                 # оптовые покупатели
employees/               # сотрудники, отделы
accounts/                # авторизация, профиль пользователя
api/                     # REST API (DRF)
templates/               # HTML-шаблоны
static/                  # CSS, JS, изображения
```

## 👥 Уровни доступа
| Роль | Права |
|------|-------|
| Анонимный | Каталог, промокоды, новости, FAQ, контакты |
| Покупатель (buyer) | + Личный кабинет, отзывы, свои заказы |
| Сотрудник (employee/staff) | + Заказы, клиенты, сотрудники |
| Администратор (superuser) | + Статистика, аналитика, Admin Panel |

## 🔌 API
- **REST API:** `/api/` (DRF browsable API)
- **Токен:** `POST /api/token/` `{"username": "...", "password": "..."}`
- Публичные endpoint'ы: `/api/furniture/`, `/api/categories/`, `/api/promos/`
- Авторизованные: `/api/orders/`, `/api/stats/`
- Только Admin: `/api/clients/`

## 🌐 Внешние API
1. **OpenWeatherMap** — погода на главной странице
2. **ExchangeRate API** (open.er-api.com) — курсы валют (бесплатно, без ключа)

## 🐳 Docker
```bash
docker build -t furniture-factory .
docker-compose up --build
```

## ☁️ Хостинг (Render.com)
1. Push на GitHub
2. New Web Service → выбрать репозиторий
3. Настройки берутся из `render.yaml`
4. Добавить PostgreSQL database в Dashboard
