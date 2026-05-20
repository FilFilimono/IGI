"""
Management command to populate the database with realistic demo data.
Run: python manage.py seed_data
"""
import random
from datetime import date, timedelta, datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace-images',
            action='store_true',
            help='Заменить фото из static/seed/ (если файлы есть) или сгенерировать заново',
        )

    def handle(self, *args, **options):
        self.replace_images = options['replace_images']
        self.stdout.write('Заполнение базы данных...')

        self._create_superuser()
        self._create_categories()
        self._create_models()
        self._create_tags()
        self._create_furniture()
        self._create_promos()
        self._create_departments()
        self._create_employees()
        self._create_clients()
        self._create_articles()
        self._create_glossary()
        self._create_vacancies()
        self._create_company_info()
        self._create_orders()
        self._create_reviews()
        self._assign_images()

        self.stdout.write(self.style.SUCCESS('✓ База данных заполнена успешно!'))

    def _create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@furniture.by', 'admin123')
            self.stdout.write('  ✓ Суперпользователь: admin / admin123')

        # Staff user (employee)
        if not User.objects.filter(username='manager1').exists():
            u = User.objects.create_user('manager1', 'manager@furniture.by', 'manager123', is_staff=True)
            u.first_name = 'Алексей'; u.last_name = 'Петров'; u.save()
        # Buyer user
        if not User.objects.filter(username='buyer1').exists():
            u = User.objects.create_user('buyer1', 'buyer@client.by', 'buyer123')
            u.first_name = 'Иван'; u.last_name = 'Сидоров'; u.save()

    def _create_categories(self):
        from catalog.models import FurnitureCategory
        cats = [
            ('Кухонная мебель', 'kitchen', 'Кухонные гарнитуры, шкафы, столы и стулья для кухни'),
            ('Кабинетная мебель', 'cabinet', 'Мебель для домашнего кабинета: столы, кресла, стеллажи'),
            ('Офисная мебель', 'office', 'Офисные столы, кресла, переговорные комплекты'),
            ('Спальная мебель', 'bedroom', 'Кровати, шкафы, комоды, тумбочки'),
            ('Мебель для гостиной', 'living', 'Диваны, кресла, журнальные столики, стенки'),
        ]
        for name, slug, desc in cats:
            FurnitureCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
        self.stdout.write('  ✓ Категории')

    def _create_models(self):
        from catalog.models import FurnitureModel
        models = ['Классик', 'Модерн', 'Эко', 'Люкс', 'Стандарт', 'Премиум', 'Бизнес', 'Комфорт']
        for name in models:
            FurnitureModel.objects.get_or_create(name=name)
        self.stdout.write('  ✓ Модели')

    def _create_tags(self):
        from catalog.models import Tag
        tags = [
            ('Хит продаж', 'hit'), ('Новинка', 'new'), ('Скидка', 'sale'),
            ('Eco-материалы', 'eco'), ('Под заказ', 'custom'), ('Антивандальный', 'antivandal'),
        ]
        for name, slug in tags:
            Tag.objects.get_or_create(slug=slug, defaults={'name': name})
        self.stdout.write('  ✓ Теги')

    def _create_furniture(self):
        from catalog.models import FurnitureItem, FurnitureCategory, FurnitureModel, Tag
        items_data = [
            # (code, name, cat_slug, model, price, active)
            ('KU-001', 'Кухонный гарнитур "Милан"', 'kitchen', 'Люкс', 2850.00, True),
            ('KU-002', 'Кухонный стол раскладной', 'kitchen', 'Классик', 450.00, True),
            ('KU-003', 'Стул кухонный "Комфорт"', 'kitchen', 'Стандарт', 89.00, True),
            ('KU-004', 'Барная стойка "Ривьера"', 'kitchen', 'Модерн', 1200.00, True),
            ('KU-005', 'Кухонный гарнитур "Прованс"', 'kitchen', 'Классик', 3200.00, True),
            ('KA-001', 'Письменный стол "Директор"', 'cabinet', 'Бизнес', 680.00, True),
            ('KA-002', 'Книжный шкаф "Библиотека"', 'cabinet', 'Классик', 920.00, True),
            ('KA-003', 'Кресло руководителя "Комфорт"', 'cabinet', 'Премиум', 540.00, True),
            ('KA-004', 'Тумба офисная 3-ящичная', 'cabinet', 'Стандарт', 210.00, True),
            ('OF-001', 'Стол переговорный 10 мест', 'office', 'Бизнес', 4500.00, True),
            ('OF-002', 'Офисное кресло "Эргон"', 'office', 'Комфорт', 320.00, True),
            ('OF-003', 'Офисный стол с тумбой', 'office', 'Стандарт', 580.00, True),
            ('OF-004', 'Шкаф для документов', 'office', 'Стандарт', 390.00, True),
            ('OF-005', 'Диван офисный двухместный', 'office', 'Модерн', 1100.00, True),
            ('SP-001', 'Кровать "Классик" 160×200', 'bedroom', 'Классик', 850.00, True),
            ('SP-002', 'Шкаф-купе трёхстворчатый', 'bedroom', 'Модерн', 1650.00, True),
            ('SP-003', 'Комод 5-ящичный', 'bedroom', 'Эко', 420.00, True),
            ('GL-001', 'Диван угловой "Релакс"', 'living', 'Комфорт', 2200.00, True),
            ('GL-002', 'Кресло-качалка "Уют"', 'living', 'Классик', 480.00, True),
            ('GL-003', 'Журнальный столик стеклянный', 'living', 'Модерн', 290.00, False),
        ]
        tag_hit = Tag.objects.get(slug='hit')
        tag_new = Tag.objects.get(slug='new')
        tag_eco = Tag.objects.get(slug='eco')

        for code, name, cat_slug, model_name, price, active in items_data:
            cat = FurnitureCategory.objects.get(slug=cat_slug)
            model = FurnitureModel.objects.get(name=model_name)
            item, created = FurnitureItem.objects.get_or_create(
                product_code=code,
                defaults={
                    'name': name, 'category': cat, 'model': model,
                    'price': Decimal(str(price)), 'is_active': active,
                    'description': f'{name} — качественное изделие из экологически чистых материалов.',
                    'dimensions': f'{random.randint(60,200)}x{random.randint(40,100)}x{random.randint(70,220)} см',
                    'material': random.choice(['МДФ', 'ЛДСП', 'Массив сосны', 'Массив дуба', 'Металл + ЛДСП']),
                    'weight': Decimal(str(round(random.uniform(15, 150), 1))),
                }
            )
            if created:
                if price > 1000:
                    item.tags.add(tag_hit)
                if code.endswith('5') or code.endswith('4'):
                    item.tags.add(tag_new)
                if 'Эко' in model_name:
                    item.tags.add(tag_eco)
        self.stdout.write('  ✓ Изделия (20 шт.)')

    def _create_promos(self):
        from catalog.models import Promo, FurnitureCategory
        now = timezone.now()
        promos = [
            ('KITCHEN10', 'percent', 10, 'Скидка 10% на кухонную мебель', True, now - timedelta(days=30), now + timedelta(days=60)),
            ('OFFICE15', 'percent', 15, 'Скидка 15% на офисную мебель', True, now - timedelta(days=10), now + timedelta(days=30)),
            ('SAVE500', 'fixed', 500, 'Скидка 500 руб. на заказ от 3000 руб.', True, now - timedelta(days=5), now + timedelta(days=90)),
            ('SUMMER20', 'percent', 20, 'Летняя акция — 20%', False, now - timedelta(days=120), now - timedelta(days=1)),
            ('NEWYEAR', 'percent', 25, 'Новогодняя скидка 25%', False, now - timedelta(days=200), now - timedelta(days=100)),
        ]
        for code, dtype, val, desc, active, vfrom, vto in promos:
            Promo.objects.get_or_create(code=code, defaults={
                'discount_type': dtype, 'discount_value': Decimal(str(val)),
                'description': desc, 'is_active': active,
                'valid_from': vfrom, 'valid_to': vto,
                'usage_limit': 100, 'used_count': random.randint(0, 50),
            })
        self.stdout.write('  ✓ Промокоды')

    def _create_departments(self):
        from employees.models import Department
        depts = [
            ('Производство', 'Изготовление мебели'),
            ('Продажи', 'Работа с клиентами и оптовыми заказами'),
            ('Дизайн', 'Разработка новых моделей'),
            ('Логистика', 'Доставка и склад'),
            ('Администрация', 'Руководство и бухгалтерия'),
        ]
        for name, desc in depts:
            Department.objects.get_or_create(name=name, defaults={'description': desc})
        self.stdout.write('  ✓ Отделы')

    def _create_employees(self):
        from employees.models import Employee, Department
        from django.contrib.auth.models import User
        staff_user = User.objects.get(username='manager1')
        prod = Department.objects.get(name='Производство')
        sales = Department.objects.get(name='Продажи')
        design = Department.objects.get(name='Дизайн')
        logist = Department.objects.get(name='Логистика')
        admin = Department.objects.get(name='Администрация')

        employees_data = [
            ('Иванов', 'Дмитрий', 'Сергеевич', 'director', admin, '+375 (17) 200-10-01', 'ivanov@furniture.by', date(1975, 3, 15), date(2000, 1, 1), 'Общее руководство фабрикой.', staff_user),
            ('Петров', 'Алексей', 'Николаевич', 'manager', sales, '+375 (29) 200-10-02', 'petrov@furniture.by', date(1985, 7, 22), date(2010, 3, 1), 'Работа с оптовыми заказчиками.', None),
            ('Сидорова', 'Наталья', 'Владимировна', 'manager', sales, '+375 (33) 200-10-03', 'sidorova@furniture.by', date(1990, 11, 5), date(2015, 6, 1), 'Продажи и ведение клиентской базы.', None),
            ('Козлов', 'Артём', 'Петрович', 'designer', design, '+375 (44) 200-10-04', 'kozlov@furniture.by', date(1993, 4, 18), date(2018, 9, 1), 'Разработка дизайна новых коллекций.', None),
            ('Михайлова', 'Елена', 'Ивановна', 'accountant', admin, '+375 (29) 200-10-05', 'mikhailova@furniture.by', date(1980, 8, 30), date(2005, 2, 1), 'Бухгалтерский учёт и отчётность.', None),
            ('Захаров', 'Павел', 'Андреевич', 'craftsman', prod, '+375 (33) 200-10-06', 'zakharov@furniture.by', date(1988, 1, 12), date(2012, 4, 1), 'Сборка кухонной и офисной мебели.', None),
            ('Новиков', 'Роман', 'Олегович', 'logist', logist, '+375 (44) 200-10-07', 'novikov@furniture.by', date(1992, 6, 25), date(2016, 7, 1), 'Организация доставки и работа со складом.', None),
        ]
        for ln, fn, mn, pos, dept, phone, email, bd, hd, desc, user in employees_data:
            emp, _ = Employee.objects.get_or_create(
                email=email,
                defaults={
                    'last_name': ln, 'first_name': fn, 'middle_name': mn,
                    'position': pos, 'department': dept, 'phone': phone,
                    'birth_date': bd, 'hire_date': hd, 'description': desc,
                    'is_active': True, 'user': user,
                }
            )
        self.stdout.write('  ✓ Сотрудники (7 чел.)')

    def _create_clients(self):
        from clients.models import Client
        from django.contrib.auth.models import User
        buyer_user = User.objects.get(username='buyer1')
        clients_data = [
            ('CL-001', 'ООО "МебельТорг"', '+375 (17) 300-10-01', 'minsk', 'ул. Ленина, 12', 'mebeltrorg@mail.by', 'Ковалёв Сергей', date(1978, 5, 10), buyer_user),
            ('CL-002', 'ИП Громов А.В.', '+375 (29) 300-10-02', 'gomel', 'ул. Советская, 45', 'gromov@tut.by', 'Громов Андрей', date(1982, 9, 20), None),
            ('CL-003', 'ООО "Интерьер Плюс"', '+375 (33) 300-10-03', 'brest', 'пр. Машерова, 7', 'interior@brest.by', 'Давыдова Марина', date(1975, 3, 15), None),
            ('CL-004', 'ЗАО "ОфисЦентр"', '+375 (44) 300-10-04', 'minsk', 'ул. Притыцкого, 100', 'office@center.by', 'Рябов Константин', date(1980, 11, 8), None),
            ('CL-005', 'ООО "Домашний уют"', '+375 (17) 300-10-05', 'vitebsk', 'ул. Кирова, 33', 'uyut@vitebsk.by', 'Зайцева Ольга', date(1990, 6, 1), None),
            ('CL-006', 'ИП Лебедев П.С.', '+375 (29) 300-10-06', 'grodno', 'ул. Советских пограничников, 22', 'lebedev@grodno.by', 'Лебедев Павел', date(1985, 4, 14), None),
            ('CL-007', 'ООО "СтильДом"', '+375 (33) 300-10-07', 'mogilev', 'ул. Первомайская, 55', 'stildom@mogilev.by', 'Макаров Виктор', date(1977, 12, 30), None),
            ('CL-008', 'ЗАО "КорпусМебель"', '+375 (44) 300-10-08', 'minsk', 'пр. Независимости, 180', 'korpus@minsk.by', 'Соловьёва Алина', date(1988, 8, 19), None),
            ('CL-009', 'ООО "ДеревоДом"', '+375 (17) 300-10-09', 'brest', 'ул. Московская, 3', 'derevo@brest.by', 'Тихонов Юрий', date(1983, 2, 7), None),
            ('CL-010', 'ИП Воробьёв Н.А.', '+375 (29) 300-10-10', 'gomel', 'ул. Хатаевича, 8', 'vorobiev@gomel.by', 'Воробьёв Никита', date(1992, 7, 16), None),
            ('CL-011', 'ООО "МаксиМебель"', '+375 (33) 300-10-11', 'vitebsk', 'ул. Ленина, 78', 'maxi@vitebsk.by', 'Кузнецова Людмила', date(1979, 10, 25), None),
            ('CL-012', 'ЗАО "ГородскойИнтерьер"', '+375 (17) 300-10-12', 'minsk', 'ул. Скрипникова, 15', 'gorod@minsk.by', 'Борисов Игорь', date(1986, 1, 3), None),
        ]
        for code, name, phone, city, addr, email, contact, bd, user in clients_data:
            Client.objects.get_or_create(client_code=code, defaults={
                'company_name': name, 'phone': phone, 'city': city,
                'address': addr, 'email': email, 'contact_person': contact,
                'birth_date': bd, 'is_active': True, 'user': user,
            })

        # Bind buyer_user client profile
        try:
            from accounts.models import UserProfile
            prof, _ = UserProfile.objects.get_or_create(user=buyer_user)
            prof.role = 'buyer'; prof.save()
        except Exception:
            pass

        self.stdout.write('  ✓ Клиенты (12 компаний)')

    def _create_articles(self):
        from main.models import Article
        articles = [
            ('Запуск новой линейки офисной мебели', 'Фабрика представляет коллекцию "Бизнес Про" 2024.', True),
            ('Участие в международной выставке мебели', 'Наша фабрика приняла участие в выставке в Москве.', True),
            ('Новые материалы: экологически чистое производство', 'Переходим на сертифицированные Eco-материалы.', True),
            ('Расширение производства: новый цех', 'Открыт новый производственный корпус площадью 2000 м².', True),
            ('Итоги 2023 года: рекордные продажи', 'Объём продаж вырос на 35% по сравнению с 2022 годом.', True),
        ]
        for i, (title, summary, published) in enumerate(articles):
            Article.objects.get_or_create(title=title, defaults={
                'summary': summary,
                'content': f'{summary}\n\nПодробная информация будет опубликована в ближайшее время.',
                'is_published': published,
                'published_at': timezone.now() - timedelta(days=i * 10),
            })
        self.stdout.write('  ✓ Статьи')

    def _create_glossary(self):
        from main.models import GlossaryTerm
        terms = [
            ('Что такое ЛДСП?', 'ЛДСП — ламинированная древесно-стружечная плита. Основной материал корпусной мебели.'),
            ('Чем МДФ отличается от ДСП?', 'МДФ более плотный и однородный, лучше держит крепёж, экологичнее.'),
            ('Что такое оптовый заказ?', 'Заказ от 5 и более единиц одного наименования с соответствующей скидкой.'),
            ('Каковы сроки изготовления?', 'Стандартный срок — 14-21 рабочий день с момента подтверждения заказа.'),
            ('Есть ли гарантия на мебель?', 'Гарантийный срок — 24 месяца на все изделия фабричного производства.'),
            ('Что такое фасад МДФ с плёнкой ПВХ?', 'Это МДФ-панель, покрытая полимерной плёнкой. Устойчива к влаге и перепадам температур.'),
            ('Каковы условия доставки?', 'Доставка осуществляется по всей Беларуси транспортными компаниями-партнёрами.'),
            ('Можно ли заказать нестандартные размеры?', 'Да, производим мебель по индивидуальным размерам с наценкой 15-20%.'),
        ]
        for q, a in terms:
            GlossaryTerm.objects.get_or_create(question=q, defaults={'answer': a})
        self.stdout.write('  ✓ Словарь терминов')

    def _create_vacancies(self):
        from main.models import Vacancy
        vacancies = [
            ('Менеджер по продажам', 'Работа с оптовыми клиентами, обработка заказов, ведение CRM.', 'Опыт от 1 года, знание ПК, грамотная речь.', 900, 1300),
            ('Мастер-сборщик мебели', 'Сборка и монтаж мебели на производстве и у клиентов.', 'Опыт от 2 лет, наличие инструмента.', 800, 1200),
            ('Дизайнер интерьера', 'Разработка проектов мебели по заказу клиентов в 3D.', 'Знание SketchUp, PRO100, базовые чертежи.', 900, 1400),
            ('Водитель-экспедитор', 'Доставка мебели по городу и области, кат. В и Е.', 'Стаж вождения от 3 лет, без вредных привычек.', 750, 1050),
        ]
        for title, desc, req, s_from, s_to in vacancies:
            Vacancy.objects.get_or_create(title=title, defaults={
                'description': desc, 'requirements': req,
                'salary_from': Decimal(str(s_from)), 'salary_to': Decimal(str(s_to)),
                'is_active': True,
            })
        self.stdout.write('  ✓ Вакансии')

    def _create_company_info(self):
        from main.models import CompanyInfo
        CompanyInfo.objects.get_or_create(
            title='О нас',
            defaults={'content': (
                'ООО "МебельФабрика" — ведущий белорусский производитель корпусной мебели.\n\n'
                'С 2000 года мы производим качественную кухонную, кабинетную и офисную мебель '
                'для оптовых покупателей по всей Беларуси и за рубежом.\n\n'
                'Наши преимущества:\n'
                '• Собственное производство площадью 5000 м²\n'
                '• Более 200 наименований в каталоге\n'
                '• Собственный конструкторский отдел\n'
                '• Экологически чистые материалы\n'
                '• Гарантия 24 месяца\n'
                '• Доставка по всей Беларуси\n\n'
                'Адрес: г. Минск, ул. Промышленная, д. 1\n'
                'Телефон: +375 (17) 200-00-01\n'
                'Email: info@furniture.by'
            )}
        )
        self.stdout.write('  ✓ О компании')

    def _create_orders(self):
        from orders.models import Order, OrderItem
        from clients.models import Client
        from catalog.models import FurnitureItem, Promo
        from employees.models import Employee

        clients = list(Client.objects.all())
        items = list(FurnitureItem.objects.filter(is_active=True))
        employees = list(Employee.objects.filter(position='manager'))
        statuses = ['delivered', 'delivered', 'delivered', 'in_production', 'confirmed', 'pending', 'cancelled']

        promo = Promo.objects.filter(is_active=True).first()

        for i in range(1, 36):
            num = f'ORD-2024-{i:03d}'
            if Order.objects.filter(order_number=num).exists():
                continue
            client = random.choice(clients)
            manager = random.choice(employees) if employees else None
            days_ago = random.randint(1, 365)
            order_dt = timezone.now() - timedelta(days=days_ago)
            order = Order.objects.create(
                order_number=num,
                client=client,
                due_date=(order_dt + timedelta(days=random.randint(14, 45))).date(),
                status=random.choice(statuses),
                manager=manager,
                promo=promo if random.random() > 0.7 else None,
                notes=f'Заказ #{i}. Доставка согласована.' if random.random() > 0.5 else '',
            )
            # Force order_date
            Order.objects.filter(pk=order.pk).update(order_date=order_dt)

            # Add 1-4 items
            chosen = random.sample(items, min(random.randint(1, 4), len(items)))
            for furniture in chosen:
                qty = random.randint(1, 10)
                OrderItem.objects.get_or_create(
                    order=order, furniture=furniture,
                    defaults={'quantity': qty, 'unit_price': furniture.price}
                )
        self.stdout.write('  ✓ Заказы (35 шт.)')

    def _create_reviews(self):
        from main.models import Review
        from django.contrib.auth.models import User
        users = list(User.objects.filter(is_superuser=False))
        reviews = [
            (5, 'Отличная мебель! Заказывали кухонный гарнитур — качество на высоте, доставили вовремя.'),
            (5, 'Работаем с фабрикой уже 5 лет. Всегда чёткое выполнение заказов и хорошее качество.'),
            (4, 'Хорошее соотношение цена-качество. Немного задержали доставку, но в целом доволен.'),
            (5, 'Лучшая фабрика в Беларуси! Офисную мебель заказывали — всё идеально.'),
            (3, 'Качество хорошее, но хотелось бы больше вариантов цветов. Буду заказывать снова.'),
            (4, 'Заказывали диван в офис. Сборщики приехали вовремя, собрали быстро. Доволен.'),
        ]
        for rating, text in reviews:
            if users:
                user = random.choice(users)
                if not Review.objects.filter(user=user, rating=rating).exists():
                    Review.objects.create(
                        user=user,
                        name=user.get_full_name() or user.username,
                        rating=rating,
                        text=text,
                        is_approved=True,
                    )
        self.stdout.write('  ✓ Отзывы')

    def _assign_images(self):
        """
        Картинки для каталога и контактов.
        1) Положите свои файлы в static/seed/furniture/ и static/seed/employees/
           (jpg, jpeg, png, webp). Имена: по коду товара (KU-001.jpg) или 1.jpg, 2.jpg …
        2) Запуск: python manage.py seed_data --replace-images
        """
        import io
        from pathlib import Path
        from PIL import Image, ImageDraw, ImageFont
        from django.conf import settings
        from django.core.files import File
        from django.core.files.base import ContentFile
        from catalog.models import FurnitureItem
        from employees.models import Employee

        seed_root = Path(settings.BASE_DIR) / 'static' / 'seed'
        furniture_files = self._collect_seed_files(seed_root / 'furniture')
        employee_files = self._collect_seed_files(seed_root / 'employees')

        furniture_colors = [
            (70, 130, 180), (34, 139, 34), (210, 105, 30),
            (128, 0, 128), (220, 20, 60), (0, 128, 128),
        ]
        employee_colors = [
            (52, 73, 94), (41, 128, 185), (39, 174, 96),
            (142, 68, 173), (211, 84, 0), (192, 57, 43), (22, 160, 133),
        ]

        def _save_placeholder(obj, field_name, text, color, size):
            img = Image.new('RGB', size, color)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
            except OSError:
                font = ImageFont.load_default()
            lines = text.split('\n')
            y = (size[1] - len(lines) * 22) // 2
            for line in lines:
                draw.text((16, y), line[:40], fill=(255, 255, 255), font=font)
                y += 22
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=85)
            buf.seek(0)
            filename = f'{getattr(obj, "product_code", None) or obj.pk}.jpg'
            getattr(obj, field_name).save(filename, ContentFile(buf.read()), save=True)

        def _save_from_file(obj, field_name, path):
            with open(path, 'rb') as fh:
                getattr(obj, field_name).save(path.name, File(fh), save=True)

        furniture_count = 0
        for i, item in enumerate(FurnitureItem.objects.all()):
            if item.image and not self.replace_images:
                continue
            src = (
                furniture_files.get(item.product_code.lower())
                or furniture_files.get(item.product_code)
                or (furniture_files.get(str(i + 1)) if furniture_files else None)
            )
            if not src and furniture_files:
                src = list(furniture_files.values())[i % len(furniture_files)]
            if src:
                _save_from_file(item, 'image', src)
            else:
                color = furniture_colors[i % len(furniture_colors)]
                _save_placeholder(item, 'image', item.name, color, (480, 320))
            furniture_count += 1

        employee_count = 0
        for i, emp in enumerate(Employee.objects.all()):
            if emp.photo and not self.replace_images:
                continue
            key = f'{emp.last_name}_{emp.first_name}'.lower()
            src = employee_files.get(key) or employee_files.get(str(i + 1))
            if not src and employee_files:
                src = list(employee_files.values())[i % len(employee_files)]
            if src:
                _save_from_file(emp, 'photo', src)
            else:
                color = employee_colors[i % len(employee_colors)]
                _save_placeholder(emp, 'photo', f'{emp.first_name}\n{emp.last_name}', color, (320, 320))
            employee_count += 1

        if furniture_count or employee_count:
            src_note = 'из static/seed/' if (furniture_files or employee_files) else 'сгенерированы'
            self.stdout.write(f'  ✓ Изображения ({src_note}): каталог {furniture_count}, сотрудники {employee_count}')

    def _collect_seed_files(self, folder):
        """Словарь имя_без_расширения -> Path для файлов в папке."""
        from pathlib import Path
        result = {}
        folder = Path(folder)
        if not folder.is_dir():
            return result
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
                result[path.stem.lower()] = path
        return result
