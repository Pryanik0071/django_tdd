import os
import time

import pytest
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

MAX_WAIT = 10


@pytest.fixture
def browser(live_server):
    """Фикстура браузера"""
    driver = webdriver.Firefox()
    staging_server = os.environ.get("STAGING_SERVER", live_server.url)
    driver.get(staging_server)
    yield driver
    driver.quit()


def wait_for_row_in_list_table(browser, row_text):
    """Ожидание строки в таблице списка"""
    start_time = time.time()
    while True:
        try:
            table = browser.find_element(By.ID, "id_list_table")
            rows = table.find_elements(By.TAG_NAME, "tr")
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)


def wait_for(browser, fn):
    """Ожидание"""
    start_time = time.time()
    while True:
        try:
            return fn()
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)
