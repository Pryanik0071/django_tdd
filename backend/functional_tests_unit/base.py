from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER', self.live_server_url)
        self.browser.get(staging_server)

    def tearDown(self):
        """Демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидание строки в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        """Ожиданиe"""
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
