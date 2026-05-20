## Регистрация на PythonAnywhere

1. Зарегистрироваться на сайте
2. Запомните имя пользователя
3. Подтвердить почту


## Подготовка проекта на вашем компьютере

1. Убедиться, что есть файл `requirements.txt`, если нет тогда выполнить команду `pip freeze > requirements.txt`
2. Откройте `settings.py` вашего проекта и внесите изменения для продакшена:
	1. `DEBUG = False`
	2. `ALLOWED_HOSTS = ['ваше_имя.pythonanywhere.com']`
	3. `STATIC_URL = '/static/'`
	4. `STATIC_ROOT = BASE_DIR / 'staticfiles'`
3. Соберите всю статику в папку `staticfiles`
	1. `python manage.py collectstatic`
4. Заходим в папку с проектов, выделяем все файлы внутри, и создаем архив





## Загрузка файлов

1. В верхнем меню нажмите **Files**.
2. Создайте папку для проекта, например `myproject`, и перейдите в неё.
3. Нажмите кнопку **Upload a file** и загрузите ваш архив с проектом.
4. После загрузки в той же папке откройте **Bash console** (кнопка **>_ Console** в верхнем меню, либо прямо из вкладки Files есть кнопка "Open Bash console here").
5. Убедитесь что вы находитесь в папке проекта ( `myproject`)
6. В открывшейся консоли распакуйте архив:
	1. `unzip ваш_архив.zip -d .`


## Виртуальное окружение и зависимости

В консоли bash:
1. Перейдите в папку проекта
	- `cd /home/ваше_имя/myproject`
2. Создайте виртуальное окружение
	- `mkvirtualenv --python=/usr/bin/python3.12 myenv`
3. Установите зависимости
	- `pip install -r requirements.txt`


## Применение миграций и статика (опционально)

Если при запаковке проекта в  zip в ней уже был файл базы данных и  настроен супер пользователь, тогда пропускаем этот шаг, иначе:
``` python
python manage.py migrate
python manage.py createsuperuser  # создайте админа по желанию
python manage.py collectstatic  # снова, если собирали дома
```


## Настройка веб-приложения

1. В верхнем меню нажмите **Web**.
2. Нажмите кнопку **Add a new web app**.
3. Нажмите **Next** в окне с вашим доменом.
4. Выберите **Manual configuration** (не Django, а именно manual).
5. Выберите версию Python (такую же, как в виртуальном окружении, например 3.12).
6. Нажмите **Next**.
7. Когда веб-приложение создастся, прокрутите вниз до раздела **Code**.
8. В строке **Source code** укажите путь к папке проекта: `/home/ваше_имя/myproject`
9. В строке **Working directory** укажите тот же путь: `/home/ваше_имя/myproject`
10. В разделе **WSGI configuration file** нажмите на ссылку с путем к файлу (откроется редактор). Удалите **весь** код, и вставить этот заменив ваше имя и название проекта в пути **path**:
``` python
import os
import sys

path = '/home/ваше_имя/myproject'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
11. Нажмите кнопку **Save** вверху справа
12. В разделе **Virtualenv** введите заменив на свое имя:
	- `/home/ваше_имя/.virtualenvs/myenv`
13. В разделе **Static files** добавьте один роут:
	- URL: `/static/`
	- Path: `/home/ваше_имя/myproject/staticfiles`
	- (Это папка, которая прописана в settings.py в поле STATIC_ROOT.)
14. Нажмите зеленую кнопку **Reload web app** на самом верху страницы.

Теперь ваше приложение должно быть доступно по адресу `https://ваше_имя.pythonanywhere.com`