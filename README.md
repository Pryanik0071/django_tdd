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
