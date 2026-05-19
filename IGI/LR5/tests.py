"""
Тесты проекта МебельФабрика
Покрытие: модели, представления, формы, API
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from catalog.models import FurnitureCategory, FurnitureModel, FurnitureItem, Tag, Promo
from clients.models import Client
from employees.models import Employee, Department
from orders.models import Order, OrderItem
from main.models import Article, GlossaryTerm, Review, Vacancy, CompanyInfo
from accounts.models import UserProfile


# =========================================================
# MODEL TESTS
# =========================================================

class FurnitureCategoryModelTest(TestCase):
    def setUp(self):
        self.cat = FurnitureCategory.objects.create(name='Кухонная', slug='kitchen')

    def test_str(self):
        self.assertEqual(str(self.cat), 'Кухонная')

    def test_slug_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(Exception):
            FurnitureCategory.objects.create(name='Кухонная 2', slug='kitchen')


class FurnitureItemModelTest(TestCase):
    def setUp(self):
        self.cat = FurnitureCategory.objects.create(name='Офисная', slug='office')
        self.model = FurnitureModel.objects.create(name='Бизнес')
        self.item = FurnitureItem.objects.create(
            product_code='OF-TEST-001',
            name='Тестовый стол',
            category=self.cat,
            model=self.model,
            price=Decimal('500.00'),
            is_active=True,
        )

    def test_str(self):
        self.assertIn('Тестовый стол', str(self.item))
        self.assertIn('OF-TEST-001', str(self.item))

    def test_product_code_unique(self):
        with self.assertRaises(Exception):
            FurnitureItem.objects.create(
                product_code='OF-TEST-001',
                name='Другой стол',
                category=self.cat,
                model=self.model,
                price=Decimal('300.00'),
            )

    def test_price_positive(self):
        self.assertGreaterEqual(self.item.price, 0)

    def test_is_active_default_true(self):
        item = FurnitureItem.objects.create(
            product_code='OF-TEST-002',
            name='Стол 2',
            category=self.cat,
            model=self.model,
            price=Decimal('300.00'),
        )
        self.assertTrue(item.is_active)


class ClientModelTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            client_code='CL-TEST-001',
            company_name='ООО Тест',
            phone='+375 (29) 100-10-01',
            city='minsk',
            address='ул. Тестовая, 1',
            birth_date=date(1985, 5, 10),
        )

    def test_str(self):
        self.assertIn('ООО Тест', str(self.client_obj))

    def test_age_calculation(self):
        age = self.client_obj.age
        self.assertIsNotNone(age)
        self.assertGreater(age, 18)

    def test_phone_format(self):
        from django.core.exceptions import ValidationError
        self.client_obj.full_clean()  # should not raise

    def test_client_code_unique(self):
        with self.assertRaises(Exception):
            Client.objects.create(
                client_code='CL-TEST-001',
                company_name='Дубликат',
                phone='+375 (29) 100-10-02',
                city='gomel',
                address='ул. Другая, 2',
            )


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name='Тест-Отдел')
        self.emp = Employee.objects.create(
            first_name='Иван', last_name='Тестов', middle_name='Петрович',
            position='manager', department=self.dept,
            phone='+375 (29) 111-11-11',
            email='test@test.by',
            birth_date=date(1990, 1, 1),
            hire_date=date(2020, 1, 1),
        )

    def test_full_name(self):
        self.assertEqual(self.emp.full_name, 'Тестов Иван Петрович')

    def test_age(self):
        self.assertGreater(self.emp.age, 18)

    def test_str(self):
        self.assertIn('Тестов Иван', str(self.emp))


class OrderModelTest(TestCase):
    def setUp(self):
        self.cat = FurnitureCategory.objects.create(name='Кухонная', slug='kitchen-ord')
        self.fmodel = FurnitureModel.objects.create(name='Тест')
        self.item = FurnitureItem.objects.create(
            product_code='T-001', name='Тест-изделие',
            category=self.cat, model=self.fmodel, price=Decimal('1000.00'),
        )
        self.client_obj = Client.objects.create(
            client_code='CL-ORD-001', company_name='ООО Орд',
            phone='+375 (29) 200-00-01', city='minsk', address='ул. 1',
        )
        self.order = Order.objects.create(
            order_number='ORD-TEST-001',
            client=self.client_obj,
            due_date=date.today() + timedelta(days=30),
            status='pending',
        )
        OrderItem.objects.create(order=self.order, furniture=self.item, quantity=3, unit_price=Decimal('1000.00'))

    def test_total_amount(self):
        self.assertEqual(self.order.total_amount, Decimal('3000.00'))

    def test_str(self):
        self.assertIn('ORD-TEST-001', str(self.order))

    def test_status_choices(self):
        valid_statuses = [s[0] for s in Order.STATUS_CHOICES]
        self.assertIn('pending', valid_statuses)
        self.assertIn('delivered', valid_statuses)


class PromoModelTest(TestCase):
    def setUp(self):
        now = timezone.now()
        self.promo_active = Promo.objects.create(
            code='TEST10', discount_type='percent', discount_value=Decimal('10'),
            valid_from=now - timedelta(days=1), valid_to=now + timedelta(days=30),
            is_active=True,
        )
        self.promo_expired = Promo.objects.create(
            code='OLD20', discount_type='percent', discount_value=Decimal('20'),
            valid_from=now - timedelta(days=60), valid_to=now - timedelta(days=1),
            is_active=True,
        )

    def test_active_promo_not_archived(self):
        self.assertFalse(self.promo_active.is_archived)

    def test_expired_promo_is_archived(self):
        self.assertTrue(self.promo_expired.is_archived)

    def test_str(self):
        self.assertIn('TEST10', str(self.promo_active))


# =========================================================
# VIEW TESTS
# =========================================================

class PublicViewsTest(TestCase):
    """Тесты публичных страниц (без авторизации)"""

    def setUp(self):
        self.client = TestClient()

    def test_home_200(self):
        r = self.client.get(reverse('main:home'))
        self.assertEqual(r.status_code, 200)

    def test_about_200(self):
        r = self.client.get(reverse('main:about'))
        self.assertEqual(r.status_code, 200)

    def test_news_200(self):
        r = self.client.get(reverse('main:news'))
        self.assertEqual(r.status_code, 200)

    def test_glossary_200(self):
        r = self.client.get(reverse('main:glossary'))
        self.assertEqual(r.status_code, 200)

    def test_contacts_200(self):
        r = self.client.get(reverse('main:contacts'))
        self.assertEqual(r.status_code, 200)

    def test_privacy_200(self):
        r = self.client.get(reverse('main:privacy'))
        self.assertEqual(r.status_code, 200)

    def test_vacancies_200(self):
        r = self.client.get(reverse('main:vacancies'))
        self.assertEqual(r.status_code, 200)

    def test_reviews_200(self):
        r = self.client.get(reverse('main:reviews'))
        self.assertEqual(r.status_code, 200)

    def test_catalog_200(self):
        r = self.client.get(reverse('catalog:item_list'))
        self.assertEqual(r.status_code, 200)

    def test_catalog_categories_200(self):
        r = self.client.get(reverse('catalog:category_list'))
        self.assertEqual(r.status_code, 200)

    def test_promo_list_200(self):
        r = self.client.get(reverse('catalog:promo_list'))
        self.assertEqual(r.status_code, 200)

    def test_login_200(self):
        r = self.client.get(reverse('accounts:login'))
        self.assertEqual(r.status_code, 200)

    def test_register_200(self):
        r = self.client.get(reverse('accounts:register'))
        self.assertEqual(r.status_code, 200)


class CatalogSearchTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        cat = FurnitureCategory.objects.create(name='Офис', slug='office-s')
        mod = FurnitureModel.objects.create(name='Тест')
        FurnitureItem.objects.create(
            product_code='S-001', name='Уникальный диван', category=cat, model=mod, price=Decimal('999'),
        )

    def test_search_found(self):
        r = self.tc.get(reverse('catalog:item_list') + '?q=Уникальный')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Уникальный')

    def test_search_not_found(self):
        r = self.tc.get(reverse('catalog:item_list') + '?q=НесуществующийТовар12345')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Ничего не найдено.')

    def test_filter_by_price(self):
        r = self.tc.get(reverse('catalog:item_list') + '?price_min=500&price_max=1500')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Уникальный диван')

    def test_filter_excludes(self):
        r = self.tc.get(reverse('catalog:item_list') + '?price_min=5000')
        self.assertNotContains(r, 'Уникальный диван')


class AuthViewsTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')
        self.superuser = User.objects.create_superuser('admin_t', 'admin@t.com', 'adminpass123')

    def test_login_success(self):
        r = self.tc.post(reverse('accounts:login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertIn(r.status_code, [200, 302])

    def test_login_wrong_pass(self):
        r = self.tc.post(reverse('accounts:login'), {'username': 'testuser', 'password': 'wrong'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Неверный логин')

    def test_profile_requires_login(self):
        r = self.tc.get(reverse('accounts:profile'))
        self.assertRedirects(r, '/accounts/login/?next=/accounts/profile/')

    def test_profile_accessible_when_logged_in(self):
        self.tc.login(username='testuser', password='testpass123')
        r = self.tc.get(reverse('accounts:profile'))
        self.assertEqual(r.status_code, 200)

    def test_statistics_requires_superuser(self):
        self.tc.login(username='testuser', password='testpass123')
        r = self.tc.get(reverse('orders:statistics'))
        self.assertEqual(r.status_code, 302)

    def test_statistics_accessible_for_superuser(self):
        self.tc.login(username='admin_t', password='adminpass123')
        r = self.tc.get(reverse('orders:statistics'))
        self.assertEqual(r.status_code, 200)

    def test_order_list_requires_login(self):
        r = self.tc.get(reverse('orders:order_list'))
        self.assertRedirects(r, '/accounts/login/?next=/orders/')

    def test_clients_requires_staff(self):
        self.tc.login(username='testuser', password='testpass123')
        r = self.tc.get(reverse('clients:client_list'))
        self.assertEqual(r.status_code, 302)  # redirected, no staff


class RegisterTest(TestCase):
    def setUp(self):
        self.tc = TestClient()

    def test_register_creates_user(self):
        r = self.tc.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'role': 'buyer',
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        r = self.tc.post(reverse('accounts:register'), {
            'username': 'baduser',
            'email': 'bad@test.com',
            'password': 'SecurePass123!',
            'password2': 'WrongPass123!',
            'role': 'buyer',
        })
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())


class ReviewTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.user = User.objects.create_user('reviewer', 'r@r.com', 'pass123')

    def test_add_review_requires_login(self):
        r = self.tc.post(reverse('main:add_review'), {'rating': 5, 'text': 'Отлично!'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_add_review_logged_in(self):
        self.tc.login(username='reviewer', password='pass123')
        r = self.tc.post(reverse('main:add_review'), {'rating': 5, 'text': 'Отличная мебель!'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)


# =========================================================
# CRUD TESTS
# =========================================================

class FurnitureItemCRUDTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.staff = User.objects.create_user('staff_u', 'staff@t.com', 'staffpass', is_staff=True)
        self.superuser = User.objects.create_superuser('super_u', 'super@t.com', 'superpass')
        self.cat = FurnitureCategory.objects.create(name='CRUD-Cat', slug='crud-cat')
        self.fmod = FurnitureModel.objects.create(name='CRUD-Mod')
        self.item = FurnitureItem.objects.create(
            product_code='CRUD-001', name='Тест CRUD', category=self.cat,
            model=self.fmod, price=Decimal('750.00'),
        )

    def test_staff_can_access_create(self):
        self.tc.login(username='staff_u', password='staffpass')
        r = self.tc.get(reverse('catalog:item_create'))
        self.assertEqual(r.status_code, 200)

    def test_staff_can_update(self):
        self.tc.login(username='staff_u', password='staffpass')
        r = self.tc.get(reverse('catalog:item_update', args=[self.item.pk]))
        self.assertEqual(r.status_code, 200)

    def test_superuser_can_delete(self):
        self.tc.login(username='super_u', password='superpass')
        r = self.tc.post(reverse('catalog:item_delete', args=[self.item.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(FurnitureItem.objects.filter(pk=self.item.pk).exists())

    def test_regular_user_cannot_create(self):
        regular = User.objects.create_user('reg_u', 'reg@t.com', 'regpass')
        self.tc.login(username='reg_u', password='regpass')
        r = self.tc.get(reverse('catalog:item_create'))
        self.assertEqual(r.status_code, 302)


# =========================================================
# FORM VALIDATION TESTS
# =========================================================

class ClientFormTest(TestCase):
    def test_valid_phone(self):
        from clients.forms import ClientForm
        data = {
            'client_code': 'CL-FORM-001',
            'company_name': 'ООО Форм',
            'phone': '+375 (29) 123-45-67',
            'city': 'minsk',
            'address': 'ул. 1',
            'is_active': True,
        }
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_phone(self):
        from clients.forms import ClientForm
        data = {
            'client_code': 'CL-FORM-002',
            'company_name': 'ООО Форм 2',
            'phone': '375291234567',  # неверный формат
            'city': 'minsk',
            'address': 'ул. 2',
            'is_active': True,
        }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_underage_contact_rejected(self):
        from clients.forms import ClientForm
        data = {
            'client_code': 'CL-FORM-003',
            'company_name': 'ООО Молодой',
            'phone': '+375 (29) 123-45-67',
            'city': 'minsk',
            'address': 'ул. 3',
            'birth_date': date.today().replace(year=date.today().year - 17).isoformat(),
            'is_active': True,
        }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)


class EmployeeFormTest(TestCase):
    def test_underage_employee_rejected(self):
        from employees.forms import EmployeeForm
        dept = Department.objects.create(name='Тест-Д')
        data = {
            'first_name': 'Юный', 'last_name': 'Работник',
            'position': 'craftsman', 'department': dept.pk,
            'phone': '+375 (29) 111-22-33',
            'email': 'young@test.by',
            'birth_date': date.today().replace(year=date.today().year - 16).isoformat(),
            'hire_date': date.today().isoformat(),
            'is_active': True,
        }
        form = EmployeeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)


# =========================================================
# API TESTS
# =========================================================

class APIPublicTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        cat = FurnitureCategory.objects.create(name='API-Cat', slug='api-cat')
        mod = FurnitureModel.objects.create(name='API-Mod')
        FurnitureItem.objects.create(
            product_code='API-001', name='API Стол', category=cat, model=mod, price=Decimal('400'),
        )

    def test_furniture_list_public(self):
        r = self.tc.get('/api/furniture/')
        self.assertEqual(r.status_code, 200)

    def test_categories_public(self):
        r = self.tc.get('/api/categories/')
        self.assertEqual(r.status_code, 200)

    def test_promos_public(self):
        r = self.tc.get('/api/promos/')
        self.assertEqual(r.status_code, 200)

    def test_orders_requires_auth(self):
        r = self.tc.get('/api/orders/')
        self.assertIn(r.status_code, [401, 403])

    def test_clients_requires_auth(self):
        r = self.tc.get('/api/clients/')
        self.assertIn(r.status_code, [401, 403])

    def test_stats_requires_auth(self):
        r = self.tc.get('/api/stats/')
        self.assertIn(r.status_code, [401, 403])


class APIAuthTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.user = User.objects.create_user('api_user', 'api@t.com', 'apipass')
        self.admin = User.objects.create_superuser('api_admin', 'apiad@t.com', 'apiadmin')
        from rest_framework.authtoken.models import Token
        self.token_user = Token.objects.create(user=self.user)
        self.token_admin = Token.objects.create(user=self.admin)

    def test_stats_with_token(self):
        r = self.tc.get('/api/stats/', HTTP_AUTHORIZATION=f'Token {self.token_user.key}')
        self.assertEqual(r.status_code, 200)

    def test_clients_requires_admin(self):
        r = self.tc.get('/api/clients/', HTTP_AUTHORIZATION=f'Token {self.token_user.key}')
        self.assertEqual(r.status_code, 403)

    def test_clients_accessible_for_admin(self):
        r = self.tc.get('/api/clients/', HTTP_AUTHORIZATION=f'Token {self.token_admin.key}')
        self.assertEqual(r.status_code, 200)


# =========================================================
# CONTEXT PROCESSOR TESTS
# =========================================================

class ContextProcessorTest(TestCase):
    def setUp(self):
        self.tc = TestClient()

    def test_date_in_context(self):
        r = self.tc.get(reverse('main:home'))
        self.assertIn('current_date_formatted', r.context)
        self.assertIn('utc_now', r.context)
        self.assertIn('user_timezone', r.context)
        self.assertIn('calendar_text', r.context)

    def test_date_format(self):
        r = self.tc.get(reverse('main:home'))
        fmt = r.context['current_date_formatted']
        parts = fmt.split('/')
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[2]), 4)  # YYYY


# =========================================================
# PARAMETRIZE-STYLE TESTS
# =========================================================

class PriceFilterParametrizedTest(TestCase):
    """Тест фильтрации по цене с разными параметрами"""

    def setUp(self):
        self.tc = TestClient()
        cat = FurnitureCategory.objects.create(name='Пар', slug='par')
        mod = FurnitureModel.objects.create(name='Пар-М')
        for i, price in enumerate([100, 500, 1000, 5000, 10000]):
            FurnitureItem.objects.create(
                product_code=f'PAR-{i:03d}', name=f'Товар {price}р',
                category=cat, model=mod, price=Decimal(str(price)),
            )

    def _filter(self, price_min=None, price_max=None):
        params = {}
        if price_min: params['price_min'] = price_min
        if price_max: params['price_max'] = price_max
        return self.tc.get(reverse('catalog:item_list'), params)

    def test_min_filter(self):
        r = self._filter(price_min=4000)
        self.assertContains(r, 'Товар 5000р')
        self.assertNotContains(r, 'Товар 100р')

    def test_max_filter(self):
        r = self._filter(price_max=200)
        self.assertContains(r, 'Товар 100р')
        self.assertNotContains(r, 'Товар 10000р')

    def test_range_filter(self):
        r = self._filter(price_min=400, price_max=600)
        self.assertContains(r, 'Товар 500р')
        self.assertNotContains(r, 'Товар 100р')
        self.assertNotContains(r, 'Товар 10000р')

    def test_no_filter_shows_all(self):
        r = self._filter()
        self.assertContains(r, 'Товар 100р')
        self.assertContains(r, 'Товар 10000р')


# =========================================================
# ADDITIONAL TESTS — clients/orders/employees CRUD views
# (to push coverage above 80%)
# =========================================================

class ClientViewsTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.staff = User.objects.create_user('staff_cl', 'sc@t.com', 'staffpass', is_staff=True)
        self.superuser = User.objects.create_superuser('super_cl', 'suc@t.com', 'superpass')
        self.client_obj = Client.objects.create(
            client_code='CL-VIEW-001', company_name='ООО Вью',
            phone='+375 (29) 123-45-67', city='minsk', address='ул. 1',
        )

    def test_client_list_staff(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.get(reverse('clients:client_list'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'ООО Вью')

    def test_client_list_search(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.get(reverse('clients:client_list') + '?q=Вью')
        self.assertContains(r, 'ООО Вью')

    def test_client_detail_staff(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.get(reverse('clients:client_detail', args=[self.client_obj.pk]))
        self.assertEqual(r.status_code, 200)

    def test_client_create_staff(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.get(reverse('clients:client_create'))
        self.assertEqual(r.status_code, 200)

    def test_client_create_post(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.post(reverse('clients:client_create'), {
            'client_code': 'CL-NEW-001', 'company_name': 'Новый клиент',
            'phone': '+375 (29) 999-88-77', 'city': 'gomel',
            'address': 'ул. Новая, 1', 'is_active': True,
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Client.objects.filter(client_code='CL-NEW-001').exists())

    def test_client_update(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.post(reverse('clients:client_update', args=[self.client_obj.pk]), {
            'client_code': 'CL-VIEW-001', 'company_name': 'ООО Вью Обновлён',
            'phone': '+375 (29) 123-45-67', 'city': 'minsk',
            'address': 'ул. Новая, 2', 'is_active': True,
        })
        self.assertEqual(r.status_code, 302)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.company_name, 'ООО Вью Обновлён')

    def test_client_delete_superuser(self):
        self.tc.login(username='super_cl', password='superpass')
        r = self.tc.post(reverse('clients:client_delete', args=[self.client_obj.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Client.objects.filter(pk=self.client_obj.pk).exists())

    def test_client_delete_requires_superuser(self):
        self.tc.login(username='staff_cl', password='staffpass')
        r = self.tc.post(reverse('clients:client_delete', args=[self.client_obj.pk]))
        self.assertEqual(r.status_code, 302)
        # still exists
        self.assertTrue(Client.objects.filter(pk=self.client_obj.pk).exists())


class OrderViewsTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.staff = User.objects.create_user('staff_ord', 'so@t.com', 'staffpass', is_staff=True)
        self.superuser = User.objects.create_superuser('super_ord', 'suo@t.com', 'superpass')
        self.cat = FurnitureCategory.objects.create(name='ОrdCat', slug='ord-cat')
        self.fmod = FurnitureModel.objects.create(name='OrdMod')
        self.item = FurnitureItem.objects.create(
            product_code='ORD-I-001', name='Ордер стол',
            category=self.cat, model=self.fmod, price=Decimal('600'),
        )
        self.client_obj = Client.objects.create(
            client_code='CL-ORD-V-001', company_name='ООО Заказ',
            phone='+375 (29) 111-22-33', city='minsk', address='ул. 1',
        )
        self.order = Order.objects.create(
            order_number='ORD-VIEW-001', client=self.client_obj,
            due_date=date.today() + timedelta(days=14), status='pending',
        )
        OrderItem.objects.create(
            order=self.order, furniture=self.item,
            quantity=2, unit_price=Decimal('600'),
        )

    def test_order_list_staff(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_list'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'ORD-VIEW-001')

    def test_order_detail_staff(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_detail', args=[self.order.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'ORD-VIEW-001')

    def test_order_total_shown(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_detail', args=[self.order.pk]))
        self.assertContains(r, '1200')  # 2 × 600

    def test_order_create_get(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_create'))
        self.assertEqual(r.status_code, 200)

    def test_order_update_get(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_update', args=[self.order.pk]))
        self.assertEqual(r.status_code, 200)

    def test_order_update_post(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.post(reverse('orders:order_update', args=[self.order.pk]), {
            'order_number': 'ORD-VIEW-001',
            'client': self.client_obj.pk,
            'due_date': (date.today() + timedelta(days=20)).isoformat(),
            'status': 'confirmed',
            'notes': '',
        })
        self.assertEqual(r.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'confirmed')

    def test_order_delete_confirm_page(self):
        self.tc.login(username='super_ord', password='superpass')
        r = self.tc.get(reverse('orders:order_delete', args=[self.order.pk]))
        self.assertEqual(r.status_code, 200)

    def test_order_delete(self):
        self.tc.login(username='super_ord', password='superpass')
        r = self.tc.post(reverse('orders:order_delete', args=[self.order.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())

    def test_order_list_filter_status(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_list') + '?status=pending')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'ORD-VIEW-001')

    def test_order_list_search(self):
        self.tc.login(username='staff_ord', password='staffpass')
        r = self.tc.get(reverse('orders:order_list') + '?q=ORD-VIEW')
        self.assertContains(r, 'ORD-VIEW-001')


class EmployeeViewsTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.staff = User.objects.create_user('staff_emp', 'se@t.com', 'staffpass', is_staff=True)
        self.dept = Department.objects.create(name='Тест-Д2')
        self.emp = Employee.objects.create(
            first_name='Тест', last_name='Сотрудник',
            position='manager', department=self.dept,
            phone='+375 (29) 555-55-55', email='emp@test.by',
            birth_date=date(1990, 1, 1), hire_date=date(2020, 1, 1),
        )

    def test_employee_list_public(self):
        r = self.tc.get(reverse('employees:employee_list'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Тест')

    def test_employee_detail(self):
        self.tc.login(username='staff_emp', password='staffpass')
        r = self.tc.get(reverse('employees:employee_detail', args=[self.emp.pk]))
        self.assertEqual(r.status_code, 200)

    def test_employee_create_get(self):
        self.tc.login(username='staff_emp', password='staffpass')
        r = self.tc.get(reverse('employees:employee_create'))
        self.assertEqual(r.status_code, 200)

    def test_employee_update_get(self):
        self.tc.login(username='staff_emp', password='staffpass')
        r = self.tc.get(reverse('employees:employee_update', args=[self.emp.pk]))
        self.assertEqual(r.status_code, 200)


class AccountsViewsExtraTest(TestCase):
    def setUp(self):
        self.tc = TestClient()
        self.user = User.objects.create_user('user_acc', 'ua@t.com', 'pass123')

    def test_logout_post(self):
        self.tc.login(username='user_acc', password='pass123')
        r = self.tc.post(reverse('accounts:logout'))
        self.assertEqual(r.status_code, 302)

    def test_redirect_if_already_logged_in(self):
        self.tc.login(username='user_acc', password='pass123')
        r = self.tc.get(reverse('accounts:login'))
        self.assertEqual(r.status_code, 302)

    def test_profile_update(self):
        self.tc.login(username='user_acc', password='pass123')
        r = self.tc.post(reverse('accounts:profile'), {
            'timezone': 'Europe/Minsk',
        })
        self.assertEqual(r.status_code, 302)

    def test_item_detail_view(self):
        cat = FurnitureCategory.objects.create(name='AccCat', slug='acc-cat')
        mod = FurnitureModel.objects.create(name='AccMod')
        item = FurnitureItem.objects.create(
            product_code='ACC-001', name='Аккаунт стол',
            category=cat, model=mod, price=Decimal('300'),
        )
        r = self.tc.get(reverse('catalog:item_detail', args=[item.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Аккаунт стол')
