run-unit-test:
	uv run manage.py test functional_tests_unit

run-pytest-test:
	uv run pytest functional_tests_pytest -v

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

format:
	uv run ruff format .

format-check:
	uv run ruff format . --check