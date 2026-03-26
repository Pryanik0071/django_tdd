from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .conftest import wait_for_row_in_list_table


def test_can_start_a_list_for_one_user(browser, live_server):
    """Можно начать список для одного пользователя"""
    # Эдит слышала про крутое новое онлайн-приложение со
    # списком неотложных дел. Она решает оценить его
    # домашнюю страницу

    # Она видит, что заголовак и шапка страницы говорят о
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

    # Страница снова обновляется и теперь показывает оба элемента ее списка
    wait_for_row_in_list_table(browser, '1: Купить павлинья перья')
    wait_for_row_in_list_table(browser, '2: Сделать мушку из перьев')

    # Удовлетворенная, она снова ложится спать.


def test_multiple_users_can_start_lists_at_different_urls(browser, live_server):
    """Многочисленные пользователи могут начать списки по разным url"""
    # Эдит начинает новый список
    input_box = browser.find_element(By.ID, 'id_new_item')
    input_box.send_keys('Купить павлинья перья')
    input_box.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, '1: Купить павлинья перья')

    # Она замечает, что её список имеет уникальный URL-адрес
    edith_list_url = browser.current_url
    assert '/lists/' in edith_list_url

    # Теперь новый пользователь, Фрэнсис, приходит на сайт.

    ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
    ## информация от Эдит не прошла через данные cookie и пр.
    browser.quit()
    browser = webdriver.Firefox()

    try:
        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        browser.get(live_server.url)
        page_text = browser.find_element(By.TAG_NAME, 'body').text
        assert 'Купить павлинья перья' not in page_text
        assert 'Сделать мушку' not in page_text

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит...
        input_box = browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        wait_for_row_in_list_table(browser, '1: Купить молоко')

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = browser.current_url
        assert '/lists/' in francis_list_url
        assert edith_list_url != francis_list_url

        # Опять-таки, нет ни следа от списка Эдит
        page_text = browser.find_element(By.TAG_NAME, 'body').text
        assert 'Купить павлинья перья' not in page_text
        assert 'Купить молоко' in page_text

        # Удовлетворенные, они оба ложатся спать
    finally:
        browser.quit()
