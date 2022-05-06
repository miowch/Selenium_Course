from utils.core_test_case import CoreTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestLinksOnCountryEditingPage(CoreTestCase):
    def test_redirects_by_links(self, driver):
        url = "http://localhost/litecart/admin/?app=countries&doc=countries"
        self.log_in_as_admin(driver, url)
        WebDriverWait(driver, 10).until(EC.title_is("Countries | My Store"))

        driver.find_element(By.CSS_SELECTOR, ".button[href$='edit_country']").click()
        WebDriverWait(driver, 10).until(EC.title_is("Add New Country | My Store"))

        main_window = driver.current_window_handle
        old_windows = driver.window_handles

        external_links = driver.find_elements(By.CSS_SELECTOR, "#content table tr a:not(a[href~='#'])")

        for external_link in external_links:
            external_link.click()

            WebDriverWait(driver, 10).until(EC.new_window_is_opened(old_windows))
            new_window = [new_window for new_window in driver.window_handles if new_window not in old_windows][0]
            driver.switch_to.window(new_window)
            driver.close()
            driver.switch_to.window(main_window)
