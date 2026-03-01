from django.test import LiveServerTestCase
import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

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

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Демонтаж"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн-приложение со
        # списком неотложных дел. Она решает оценить его
        # домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовак и шапка страницы говорят о
        # списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле - Купить павлинья перья
        input_box.send_keys('Купить павлинья перья')

        # Когда нажимаем Enter - страница обновляется и теперь появляется элемент списка
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлинья перья')

        # Добавим еще один элемент - Сделать мушку из перьев
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Сделать мушку из перьев')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Сделать мушку из перьев')
        self.wait_for_row_in_list_table('1: Купить павлинья перья')

        self.fail('Закончить тест')
