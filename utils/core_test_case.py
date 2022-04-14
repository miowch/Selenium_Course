from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest


class CoreTestCase:
    @pytest.fixture
    def driver(self, request):
        wd = webdriver.Chrome()
        request.addfinalizer(wd.quit)
        return wd

    @staticmethod
    def log_in_as_admin(driver, url):
        driver.get(url)
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.NAME, "login").click()

    @pytest.fixture
    def no_captcha(self, driver):
        url = "http://localhost/litecart/admin/?" \
              "app=settings&doc=security&" \
              "setting_group_key=store_info&" \
              "page=1&action=edit&key=captcha_enabled"
        self.log_in_as_admin(driver, url)
        driver.find_element(By.CSS_SELECTOR, "form[name='settings_form']  input[value='0']").click()
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        captcha_setting_value = driver.find_element(By.CSS_SELECTOR, "span[title$='CAPTCHA security.']")\
            .get_attribute("textContent")
        assert captcha_setting_value == "False", "CAPTCHA setting was not turned off."
