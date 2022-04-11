import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://www.google.com/")
    '''
    driver.find_element(By.NAME, "q").send_keys("webdriver")
    driver.find_element(By.NAME, "btnG").click()
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))
    '''
