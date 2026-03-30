from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .conftest import get_item_input_box, wait_for, wait_for_row_in_list_table


def test_cannot_add_empty_list_items(browser, live_server):
    """Нельзя добавлять пустые элементы списка"""
    # Эдит открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.
    # Она нажимает Enter на пустом поле ввода
    browser.get(live_server.url)
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # Браузер перехватывает запрос и не загружает страницу со списком
    wait_for(
        lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
    )

    # Эдит начинает набирать текст нового элемента и ошибка исчезает
    get_item_input_box(browser).send_keys("Buy milk")
    wait_for(
        lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
    )

    # И она может отправить его успешно
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    # Как ни странно, Эдит решает отправить второй пустой элемент списка
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # И снова браузер не подчинится
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for(
        lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
    )

    # И она может его исправить, заполнив поле неким текстом
    get_item_input_box(browser).send_keys("Make tea")
    wait_for(
        lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
    )
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for_row_in_list_table(browser, "2: Make tea")
