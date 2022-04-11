from selenium.webdriver.common.by import By


class CoreTestCase:
    @staticmethod
    def log_in_as_admin(driver, url):
        driver.get(url)
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.NAME, "login").click()
