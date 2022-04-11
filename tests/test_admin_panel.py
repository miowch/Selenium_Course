import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.core_test_case import CoreTestCase


class TestAdminPanel(CoreTestCase):
    @pytest.fixture
    def driver(self, request):
        wd = webdriver.Chrome()
        request.addfinalizer(wd.quit)
        return wd

    def test_headers_in_sidebar_menu(self, driver):
        url = "http://localhost/litecart/admin/"

        self.log_in_as_admin(driver, url)
        WebDriverWait(driver, 10).until(EC.title_is("My Store"))

        menu_sections_number = len(driver.find_elements(By.CSS_SELECTOR, "#box-apps-menu > li"))

        for i in range(menu_sections_number):
            menu_section = driver.find_elements(By.ID, "app-")[i]
            menu_section.click()
            self.check_header(driver)

            section_items = driver.find_elements(By.CSS_SELECTOR, "[id ^= doc-]")

            if section_items:
                for n in range(len(section_items)):
                    driver.find_elements(By.CSS_SELECTOR, "[id ^= doc-]")[n].click()
                    self.check_header(driver)

    @staticmethod
    def check_header(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1")))
