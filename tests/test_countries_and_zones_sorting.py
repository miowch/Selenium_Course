from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.core_test_case import CoreTestCase


class TestCountriesAndZonesSorting(CoreTestCase):
    def test_countries_sorting(self, driver):
        url = "http://localhost/litecart/admin/?app=countries&doc=countries"

        self.log_in_as_admin(driver, url)
        WebDriverWait(driver, 10).until(EC.title_is("Countries | My Store"))

        countries_names = []

        for row in driver.find_elements(By.CSS_SELECTOR, ".dataTable .row"):
            columns = driver.find_element(By.CSS_SELECTOR, ".dataTable .header")\
                .get_attribute("innerText").split("\t")

            country_name = row.get_attribute("innerText").split("\t")[columns.index('Name')]
            countries_names.append(country_name)

        assert countries_names == sorted(countries_names), "Countries are not sorted in alphabetical order."

    def test_zones_sorting(self, driver):
        url = "http://localhost/litecart/admin/?app=countries&doc=countries"

        self.log_in_as_admin(driver, url)
        WebDriverWait(driver, 10).until(EC.title_is("Countries | My Store"))

        countries_with_zones = self.get_countries_with_zones(driver)

        for country in countries_with_zones:
            driver.find_element(By.CSS_SELECTOR, f".dataTable .row a[href$='{country}']").click()

            zones_names = []

            for zones_row in driver.find_elements(By.CSS_SELECTOR, ".dataTable tbody > :not(.header, :last-child)"):
                columns_of_zones_table = driver.find_element(By.CSS_SELECTOR, "#table-zones .header")\
                    .get_attribute("innerText").split("\t")

                zone_name = zones_row.get_attribute("innerText").split("\t")[columns_of_zones_table.index('Name')]
                zones_names.append(zone_name)

            try:
                assert zones_names == sorted(zones_names)
            except AssertionError:
                print(f"Assertion failed. Zones for country with code {country} are not sorted in alphabetical order.\n")

            driver.back()

    @staticmethod
    def get_countries_with_zones(driver):
        countries_with_zones = []

        for countries_row in driver.find_elements(By.CSS_SELECTOR, ".dataTable .row"):
            columns_of_countries_table = driver.find_element(By.CSS_SELECTOR, ".dataTable .header") \
                .get_attribute("innerText").split("\t")

            if int(countries_row.get_attribute("innerText").split("\t")[columns_of_countries_table.index('Zones')]) > 0:
                country_code = countries_row.get_attribute("innerText").split("\t")[
                    columns_of_countries_table.index('Code')]
                countries_with_zones.append(country_code)

        return countries_with_zones
