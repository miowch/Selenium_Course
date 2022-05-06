from utils.core_test_case import CoreTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class TestProductCart(CoreTestCase):
    def test_adding_and_deleting_products(self, driver):
        wait = WebDriverWait(driver, 10)
        i = 0

        self.open_main_page(driver)

        while i < 3:
            driver.find_element(By.CSS_SELECTOR, "#box-most-popular .products > :first-child > .link").click()

            initial_cart_counter_value = driver.find_element(By.CSS_SELECTOR, "#header #cart .quantity").text

            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".buy_now button[name='add_cart_product']")))
            if driver.find_elements(By.CSS_SELECTOR, "select[name='options[Size]']"):
                select_size = Select(
                    driver.find_element(By.CSS_SELECTOR, "select[name='options[Size]']"))
                select_size.select_by_index(1)
            driver.find_element(By.CSS_SELECTOR, ".buy_now button[name='add_cart_product']").click()

            self.wait_until_cart_counter_gets_updated(wait, initial_cart_counter_value)
            driver.back()
            i += 1
        else:
            driver.find_element(By.CSS_SELECTOR, "#cart .link").click()

        while driver.find_elements(By.CSS_SELECTOR, "#box-checkout-cart .items > .item"):
            order_summary_table = driver.find_element(By.CSS_SELECTOR, "#order_confirmation-wrapper > .dataTable")
            driver.find_element(By.CSS_SELECTOR, "button[name='remove_cart_item']").click()
            wait.until(
                EC.staleness_of(order_summary_table)
            )

    @staticmethod
    def wait_until_cart_counter_gets_updated(wait, current_cart_counter_value):
        wait.until_not(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#header #cart .quantity"), current_cart_counter_value)
        )
