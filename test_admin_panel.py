import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_headers_in_sidebar_menu(driver):
    log_in_to_admin(driver)

    menu_sections_number = len(driver.find_elements(By.CSS_SELECTOR, "#box-apps-menu > li"))

    for i in range(menu_sections_number-1):
        menu_section = driver.find_elements(By.ID, "app-")[i]
        menu_section.click()
        check_header(driver)

        section_items = driver.find_elements(By.CLASS_NAME, "docs")

        if section_items:
            for n in range(len(section_items)-1):
                section_items[n].click()
                check_header(driver)


def log_in_to_admin(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.NAME, "login").click()
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))


def check_header(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1")))
