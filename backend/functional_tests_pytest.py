import pytest
from selenium import webdriver


@pytest.fixture
def browser():
    """Фикстура браузера"""
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


def test_can_start_a_list_and_retrieve_it_later(browser):
    """Тест: можно начать список и получить его позже"""
    # Эдит слышала про крутое новое онлайн-приложение со
    # списком неотложных дел. Она решает оценить его
    # домашнюю страницу
    browser.get('http://localhost:8000')

    # Она видит, что заголовок и шапка страницы говорят о
    # списках неотложных дел
    assert 'To-Do' in browser.title
    pytest.fail('Закончить тест')