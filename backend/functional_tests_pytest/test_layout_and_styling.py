from selenium.webdriver.common.keys import Keys

from .conftest import get_item_input_box, wait_for_row_in_list_table


def test_layout_and_styling(browser, live_server):
    """Макет и стилевое оформление"""
    # Эдит открывает домашнюю страницу
    browser.set_window_size(1024, 768)

    # Она замечает, что поле ввода аккуратно центрированно
    input_box = get_item_input_box(browser)
    assert abs(input_box.location["x"] + input_box.size["width"] / 2 - 512) < 10

    # Она начинает новый и список и видит, что поле ввода там тоже центрировано
    # centered there too
    input_box.send_keys("testing")
    input_box.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: testing")
    input_box = get_item_input_box(browser)
    assert abs(input_box.location["x"] + input_box.size["width"] / 2 - 512) < 10
