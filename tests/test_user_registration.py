from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from utils.core_test_case import CoreTestCase
from faker import Faker


class TestUserRegistration(CoreTestCase):
    @pytest.fixture
    def driver(self, request):
        wd = webdriver.Chrome()
        request.addfinalizer(wd.quit)
        return wd

    @pytest.fixture
    def no_captcha(self, driver):
        self.turn_off_captcha(driver)

    @pytest.fixture
    def user_data(self):
        return {
            "email": self.create_unique_email(),
            "pwd": "test"
        }

    def test_user_registration(self, driver, no_captcha, user_data):
        url = "http://localhost/litecart/en/create_account"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.title_is("Create Account | My Store"))

        self.create_account(driver, user_data["email"], user_data["pwd"])
        self.log_out(driver)
        self.log_in(driver, user_data["email"], user_data["pwd"])
        self.log_out(driver)

    @staticmethod
    def create_unique_email():
        random_part_email = datetime.now().strftime("%m%d%Y%H%M%S")
        return f"seleniumstc+{random_part_email}@example.com"

    @staticmethod
    def fill_in_mandatory_fields(driver, email, pwd):
        fake = Faker()

        driver.find_element(By.CSS_SELECTOR, "input[name='firstname']").send_keys(fake.first_name())
        driver.find_element(By.CSS_SELECTOR, "input[name='lastname']").send_keys(fake.last_name())
        driver.find_element(By.CSS_SELECTOR, "input[name='address1']").send_keys(fake.street_address())
        driver.find_element(By.CSS_SELECTOR, "input[name='postcode']").send_keys("10026")
        driver.find_element(By.CSS_SELECTOR, "input[name='city']").send_keys("New York")

        us_index = driver.find_element(By.CSS_SELECTOR, "select[name='country_code'] option[value='US']")\
            .get_attribute("index")
        select_country = driver.find_element(By.CSS_SELECTOR, "select[name='country_code']")
        driver.execute_script(
            f"arguments[0].selectedIndex = {us_index}; arguments[0].dispatchEvent(new Event('change'))", select_country)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='zone_code']")))
        select_zone = Select(driver.find_element(By.CSS_SELECTOR, "select[name='zone_code']"))
        select_zone.select_by_value("NY")

        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[name='phone']").send_keys(fake.phone_number())
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(pwd)
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmed_password']").send_keys(pwd)

    def create_account(self, driver, email, pwd):
        self.fill_in_mandatory_fields(driver, email, pwd)
        driver.find_element(By.CSS_SELECTOR, "button[name='create_account']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-account")))

    @staticmethod
    def log_in(driver, email, pwd):
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(pwd)
        driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-account")))

    @staticmethod
    def log_out(driver):
        driver.find_element(By.CSS_SELECTOR, "#box-account a[href$='logout']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-account-login")))
