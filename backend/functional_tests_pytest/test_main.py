import time

import pytest
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


def wait_for_row_in_list_table(browser, row_text):
    """Ожидание строки в таблице списка"""
    start_time = time.time()
    while True:
        try:
            table = browser.find_element(By.ID, 'id_list_table')
            rows = table.find_elements(By.TAG_NAME, 'tr')
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)


def test_can_start_a_list_and_retrieve_it_later(browser, live_server):
    """Тест: можно начать список и получить его позже"""
    # Эдит слышала про крутое новое онлайн-приложение со
    # списком неотложных дел. Она решает оценить его
    # домашнюю страницу
    browser.get(live_server.url)

    # Она видит, что заголовок и шапка страницы говорят о
    # списках неотложных дел
    assert 'To-Do' in browser.title
    header_text = browser.find_element(By.TAG_NAME, 'h1').text
    assert 'To-Do' in header_text

    # Ей сразу же предлагается ввести элемент списка
    input_box = browser.find_element(By.ID, 'id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

    # Она набирает в текстовом поле - Купить павлинья перья
    input_box.send_keys('Купить павлинья перья')

    # Когда нажимаем Enter - страница обновляется и теперь появляется элемент списка
    input_box.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, '1: Купить павлинья перья')

    # Добавим еще один элемент - Сделать мушку из перьев
    input_box = browser.find_element(By.ID, 'id_new_item')
    input_box.send_keys('Сделать мушку из перьев')
    input_box.send_keys(Keys.ENTER)

    wait_for_row_in_list_table(browser, '2: Сделать мушку из перьев')
    wait_for_row_in_list_table(browser, '1: Купить павлинья перья')

    pytest.fail('Закончить тест')
