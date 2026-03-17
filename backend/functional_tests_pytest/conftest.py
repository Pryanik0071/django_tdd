import os

import pytest
from selenium import webdriver


@pytest.fixture
def browser(live_server):
    """Фикстура браузера"""
    driver = webdriver.Firefox()
    staging_server = os.environ.get('STAGING_SERVER', live_server.url)
    driver.get(staging_server)
    yield driver
    driver.quit()
