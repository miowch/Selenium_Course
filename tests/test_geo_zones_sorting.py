import pytest as pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.core_test_case import CoreTestCase


class TestGeoZonesSorting(CoreTestCase):
    @pytest.fixture
    def driver(self, request):
        wd = webdriver.Chrome()
        request.addfinalizer(wd.quit)
        return wd

    def test_geo_zones_sorting(self, driver):
        url = "http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones"

        self.log_in_as_admin(driver, url)
        WebDriverWait(driver, 10).until(EC.title_is("Geo Zones | My Store"))

        countries_ids = self.get_countries_ids(driver)

        for country_id in countries_ids:
            driver.find_element(By.CSS_SELECTOR, f".dataTable .row a[href*='{country_id}']").click()

            country = driver.find_element(By.CSS_SELECTOR, "form[name='form_geo_zone'] > table input[name='name']")\
                .get_attribute("value")

            zones_names = []

            for zones_row in driver.find_elements(By.CSS_SELECTOR, "#table-zones tbody > :not(.header, :last-child)"):
                selected_zone = zones_row.find_element(By.CSS_SELECTOR, "select[name^='zones'] > option[selected='selected']")\
                    .get_attribute("textContent")

                zones_names.append(selected_zone)

            try:
                assert zones_names == sorted(zones_names)
            except AssertionError:
                print(f"Assertion failed. Zones for {country} are not sorted in alphabetical order.\n")

            driver.back()

    @staticmethod
    def get_countries_ids(driver):
        countries_ids = []

        for countries_row in driver.find_elements(By.CSS_SELECTOR, ".dataTable .row"):
            columns_of_geo_zones_table = driver.find_element(By.CSS_SELECTOR, ".dataTable .header") \
                .get_attribute("innerText").split("\t")

            country_id = countries_row.get_attribute("innerText").split("\t")[
                columns_of_geo_zones_table.index('ID')]
            countries_ids.append(country_id)

        return countries_ids
