from datetime import datetime
from os.path import abspath
from utils.core_test_case import CoreTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class TestProductAdding(CoreTestCase):
    def test_add_product(self, driver):
        url = "http://localhost/litecart/admin/?app=catalog&doc=catalog"
        self.log_in_as_admin(driver, url)
        WebDriverWait(driver, 10).until(EC.title_is("Catalog | My Store"))

        driver.find_element(By.CSS_SELECTOR, ".button[href$='edit_product']").click()
        WebDriverWait(driver, 10).until(EC.title_is("Add New Product | My Store"))

        # GENERAL TAB
        product_name = f"Test {datetime.now().strftime('%m%d%Y%H%M%S')}"
        self.fill_in_general_data(driver, product_name)

        driver.find_element(By.CSS_SELECTOR, "a[href='#tab-information']").click()

        # INFORMATION TAB
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".active a[href='#tab-information']")))
        self.fill_in_information_data(driver, product_name)

        driver.find_element(By.CSS_SELECTOR, "a[href='#tab-prices']").click()

        # PRICES TAB
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".active a[href='#tab-prices']")))
        self.fill_in_prices_data(driver, "3.50", "5")

        driver.find_element(By.CSS_SELECTOR, "button[name='save']").click()
        WebDriverWait(driver, 10).until(EC.title_is("Catalog | My Store"))

        columns_of_catalog_table = driver.find_element(By.CSS_SELECTOR, ".dataTable .header").get_attribute("innerText").split("\t")

        last_product_in_catalog = driver.find_element(By.CSS_SELECTOR, "form[name='catalog_form'] .dataTable tbody > :nth-last-child(2)")
        product_name_in_catalog = last_product_in_catalog.get_attribute("innerText").split("\t")[columns_of_catalog_table.index('Name')]

        assert product_name_in_catalog == f" {product_name}", \
            f"Product name in catalog differs from the expected '{product_name}'."

    @staticmethod
    def fill_in_general_data(driver, product_name):
        driver.find_element(By.CSS_SELECTOR, "input[name='status'][value='1']").click()
        driver.find_element(By.CSS_SELECTOR, "input[name='name[en]']").send_keys(product_name)
        driver.find_element(By.CSS_SELECTOR, "input[name='code']").send_keys("test")
        driver.find_element(By.CSS_SELECTOR, "input[name='product_groups[]'][value='1-3']").click()
        driver.find_element(By.CSS_SELECTOR, "input[name='quantity']").clear()
        driver.find_element(By.CSS_SELECTOR, "input[name='quantity']").send_keys("1")
        driver.find_element(By.CSS_SELECTOR, "input[name='new_images[]']") \
            .send_keys(f"{abspath('../utils/test_product_image.png')}")
        driver.find_element(By.CSS_SELECTOR, "input[name='date_valid_from']").send_keys(
            datetime.today().strftime("01-01-%Y"))
        driver.find_element(By.CSS_SELECTOR, "input[name='date_valid_to']").send_keys(
            datetime.today().strftime("31-12-%Y"))

    @staticmethod
    def fill_in_information_data(driver, product_name):
        select_manufacturer = Select(driver.find_element(By.CSS_SELECTOR, "select[name='manufacturer_id']"))
        select_manufacturer.select_by_visible_text("ACME Corp.")

        driver.find_element(By.CSS_SELECTOR, "input[name='keywords']").send_keys("test_product")
        driver.find_element(By.CSS_SELECTOR, "input[name='short_description[en]']").send_keys("test product adding")
        driver.find_element(By.CSS_SELECTOR, ".trumbowyg-editor").send_keys("Description: Test product adding")
        driver.find_element(By.CSS_SELECTOR, "input[name='head_title[en]']").send_keys(f"head title {product_name}")
        driver.find_element(By.CSS_SELECTOR, "input[name='meta_description[en]']") \
            .send_keys(f"meta description {product_name}")

    @staticmethod
    def fill_in_prices_data(driver, purchase_price, price):
        driver.find_element(By.CSS_SELECTOR, "input[name='purchase_price']").clear()
        driver.find_element(By.CSS_SELECTOR, "input[name='purchase_price']").send_keys(f"{purchase_price}")
        select_price_currency = Select(
            driver.find_element(By.CSS_SELECTOR, "select[name='purchase_price_currency_code']"))
        select_price_currency.select_by_value("EUR")
        driver.find_element(By.CSS_SELECTOR, "input[name='prices[EUR]']").send_keys(f"{price}")
