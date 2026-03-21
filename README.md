Some comment

`uv sync` # Without test group dep

`uv sync --group test`

`uv run pytest functional_tests_pytest.py -v` - Запустить функциональные тесты

`uv run manage.py test` - Запустить тесты модульные (Django)

`uv run manage.py test functional_tests` - Запуск unit тестов через manage.py и LiveServer Django

Функциональные тесты - проверяют приложени с точки зрения пользователя, внешней стороны
Модульные - с точки зрения программиста, изнутри

БД для тестов - одна на весь прогон, новая. Но откатывается между тестами (транзакциями)

TDD: Функциональный тест -> Модульный тест -> Прикладной код

run-unit-test: Запуск unit тестов через manage.py и LiveServer Django
uv run manage.py test functional_tests_unit

run-pytest-test: Запустить функциональные тесты pytest
uv run pytest functional_tests_pytest -v

Запуск всех тестов через manage.py (unit test функциональные + модульные в приложении) - uv run manage.py test (app) - все приложения или app.lists (только приложение lists)

LiveServer для изоляции БД во время функциональных тестов + убрали time.sleep(). Автор книги против внутренних функций wait элемента. Но это для Selenium 3, нужно посмотреть, как 4 работает с ожиданием (неявным). Явное ожидание - плохо.

REST - разделение обязанноестей. Каждый URL отвечает за одно дейтсвие

https://www.obeythetestinggoat.com/

## Nginx

- apt-get install nginx
- systemctl start nginx

**Path to save - /etc/nginx/sites-available**

```nginx -
    server {
        listen 80;
        server_name domain_name;

        location / {
            proxy_pass http://localhost:8000;
        }
    }
```

**Отдавать статику через Nginx**

- collect static --noinput
- Установить gunicorn и запустить через venv/bin/gunicorn app.wsgi:application? - CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]
- reload nginx

```nginx

    location /static {
        alias /home/elspeth/sites/app/static; (Path to static)
    }

```

Веб-сервер будет прослушивать только наш домен и проксировать все запросы на localhost

- echo $SITENAME
- ln -s ../sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME

Это сохранени конфигурации Nginx - реальный файл лежит в available, а символьная ссылка в enabled

Удалить default!

- systemctl reload nginx

Запустить службу + сервер

### Unix socket
```nginx
    
    location / {
        proxy_set_heade Host $host;
        proxy_pass http://unix:/tmp/$SITENAME.socket;
    }
```
+ gunicorn --bind unix:/tmp/$SITENAME.socket config.wsgi:application

## Настройка Systemd
Проверка, что unicorn стартует при начальной загрузке

/etc/systemd/system/gunicorn-add

```systemd
    [unit]
    Description=Gunicorn server for our app (domain) / other?
    
    [Service]
    Restart=on-failure
    User=our_user
    WorkingDirectory=Текущий рабочий каталог ? app/source?
    ExecStart=оманда запуска gunicorn?
    
    [Install]
    WantedBy=multt-user.targer - Служба запускалась на начальной загрузке
```

Сценарии лежат в /etc/systemd/system их имена заканчиваются на .service

**Поручаем Systemd загрузить новый файл конфигурации**
+ systemctl daemon-reload
+ systemctl enable (service_name)
+ systemctl start (service_name)