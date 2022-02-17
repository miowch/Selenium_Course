import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_product_sticker(driver):
    driver.get("http://localhost/litecart/en/")
    WebDriverWait(driver, 10).until(EC.title_is("Online Store | My Store"))

    products = driver.find_elements(By.CSS_SELECTOR, ".content .box [class~=product]")

    for product in products:
        try:
            sticker = product.find_elements(By.CSS_SELECTOR, "[class~=sticker]")
            if len(sticker) != 1:
                print(f"Product {product.find_element(By.CLASS_NAME, 'name').text} has {len(sticker)} stickers!")
            else:
                EC.visibility_of(sticker)
        except NoSuchElementException:
            print(f"Product {product.find_element(By.CLASS_NAME, 'name').text} doesn't have a sticker.")
