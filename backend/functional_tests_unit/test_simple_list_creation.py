from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    """Тест нового посетителя"""

    def test_can_start_a_list_for_one_user(self):
        """Можно начать список для одного пользователя"""
        # Эдит слышала про крутое новое онлайн-приложение со
        # списком неотложных дел. Она решает оценить его
        # домашнюю страницу

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
