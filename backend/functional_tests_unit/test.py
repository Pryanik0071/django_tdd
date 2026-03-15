from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
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

    def test_can_start_a_list_for_one_user(self):
        """Можно начать список для одного пользователя"""
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

        # Страница снова обновляется и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_table('1: Купить павлинья перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из перьев')

        # Удовлетворенная, она снова ложится спать.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Купить павлинья перья')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлинья перья')

        # Она замечает, что её список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Теперь новый пользователь, Фрэнсис, приходит на сайт.

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлинья перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит...
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(edith_list_url, francis_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлинья перья', page_text)
        self.assertIn('Купить молоко', page_text)

        # Удовлетворенные, они оба ложатся спать

    def test_layout_and_styling(self):
        """Макет и стилевое оформление"""
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно центрированно
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            input_box.location["x"] + input_box.size["width"] / 2,
            512,
            delta=10,
        )

        # Она начинает новый и список и видит, что поле ввода там тоже центрировано
        # centered there too
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            input_box.location["x"] + input_box.size["width"] / 2,
            512,
            delta=10,
        )
