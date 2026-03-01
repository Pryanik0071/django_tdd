run-unit-test:
	uv run manage.py test functional_tests_unit

run-pytest-test:
	uv run pytest functional_tests_pytest -v