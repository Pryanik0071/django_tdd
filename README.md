Some comment

`uv sync` # Without test group dep
`uv sync --group test`
`uv run pytest functional_tests_pytest.py -v`

Функциональные тесты - проверяют приложени с точки зрения пользователя, внешней стороны
Модульные - с точки зрения программиста, изнутри

TDD: Функциональный тест -> Модульный тест -> Прикладной код