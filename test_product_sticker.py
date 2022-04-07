import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_product_sticker(driver):
    driver.get("http://localhost/litecart/en/")
    WebDriverWait(driver, 10).until(EC.title_is("Online Store | My Store"))

    products = driver.find_elements(By.CSS_SELECTOR, ".content .box .product")

    for product in products:
        stickers = product.find_elements(By.CLASS_NAME, "sticker")
        if len(stickers) == 0:
            print(f"Product {product.find_element(By.CLASS_NAME, 'name').text} doesn't have a sticker.")
        elif len(stickers) > 1:
            print(f"Product {product.find_element(By.CLASS_NAME, 'name').text} has {len(stickers)} stickers!")
