import pytest
from selenium import webdriver


@pytest.fixture
def browser():
    """Фикстура браузера"""
    driver = webdriver.Firefox()
    yield driver
    driver.quit()
