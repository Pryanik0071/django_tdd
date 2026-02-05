import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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
    header_text = browser.find_element(By.TAG_NAME, 'h1').text
    assert 'To-Do' in header_text

    # Ей сразу же предлагается ввести элемент списка
    input_box = browser.find_element(By.ID, 'id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

    # Она набирает в текстовом поле - Купить павлинья перья
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    table = browser.find_element(By.ID, 'id_list_table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    assert any(row.text == '1: Купить павлинья перья' for row in rows)

    pytest.fail('Закончить тест')