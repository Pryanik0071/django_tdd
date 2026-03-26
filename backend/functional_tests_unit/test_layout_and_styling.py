from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    """Тест макета и стилевого оформления"""

    def test_layout_and_styling(self):
        """Макет и стилевое оформление"""
        # Эдит открывает домашнюю страницу
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно центрированно
        input_box = self.browser.find_element(By.ID, "id_new_item")
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
