import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome("./chromedriver")
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://www.google.com/")
    '''
    driver.find_element(By.NAME, "q").send_keys("webdriver")
    driver.find_element(By.NAME, "btnG").click()
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))
    '''
