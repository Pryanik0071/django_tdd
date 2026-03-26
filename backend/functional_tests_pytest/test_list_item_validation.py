from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .conftest import wait_for, wait_for_row_in_list_table


def test_cannot_add_empty_list_items(browser, live_server):
    """Нельзя добавлять пустые элементы списка"""
    # Эдит открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.
    # Она нажимает Enter на пустом поле ввода
    browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

    # Домашняя страница обновляется, и появляется сообщение об ошибке,
    # которое говорит, что элементы списка не должны быть пустыми
    wait_for(
        browser,
        lambda: assert_element_text(browser, ".invalid-feedback", "You can't have an empty list item"),
    )

    # Она пробует снова, теперь с неким текстом для элемента, и теперь
    # это срабатывает
    browser.find_element(By.ID, "id_new_item").send_keys("Purchase milk")
    browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Purchase milk")

    # Как ни странно, Эдит решает отправить второй пустой элемент списка
    browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

    # Она получает аналогичное предупреждение на странице списка
    wait_for(
        browser,
        lambda: assert_element_text(browser, ".invalid-feedback", "You can't have an empty list item"),
    )

    # И она может его исправить, заполнив поле неким текстом
    browser.find_element(By.ID, "id_new_item").send_keys("Make tea")
    browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "2: Make tea")


def assert_element_text(browser, css_selector, expected_text):
    """Проверка текста элемента по CSS-селектору"""
    element = browser.find_element(By.CSS_SELECTOR, css_selector)
    assert element.text == expected_text
