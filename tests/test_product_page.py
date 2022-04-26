import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.core_test_case import CoreTestCase


class TestProductPage(CoreTestCase):
    @pytest.fixture
    def product_main_page(self, driver):
        self.open_main_page(driver)
        regular_price = driver.find_element(By.CSS_SELECTOR, "#box-campaigns .content .product .regular-price")
        regular_price_font_size = regular_price.value_of_css_property("font-size")
        campaign_price = driver.find_element(By.CSS_SELECTOR, "#box-campaigns .content .product .campaign-price")
        campaign_price_font_size = campaign_price.value_of_css_property("font-size")

        product = {
            "name": driver.find_element(By.CSS_SELECTOR, "#box-campaigns .content .product .name").get_attribute("textContent"),
            "regular_price": {
                "value": regular_price.get_attribute("textContent"),
                "is_strikethrough": True if regular_price.tag_name == "s" else False,
                "is_grey": self.is_grey(regular_price.value_of_css_property("color")),
                "font_size": float(regular_price_font_size[:regular_price_font_size.find("px")])
            },
            "campaign_price": {
                "value": campaign_price.get_attribute("textContent"),
                "is_bold": True if campaign_price.tag_name == "strong" else False,
                "is_red": self.is_red(campaign_price.value_of_css_property("color")),
                "font_size": float(campaign_price_font_size[:campaign_price_font_size.find("px")])
            }
        }

        return product

    @pytest.fixture
    def product_page(self, driver):
        self.open_main_page(driver)
        driver.find_element(By.CSS_SELECTOR, "#box-campaigns .content .product .link").click()
        WebDriverWait(driver, 10).until(EC.title_contains("Subcategory"))

        regular_price = driver.find_element(By.CSS_SELECTOR, "#box-product .information .regular-price")
        regular_price_font_size = regular_price.value_of_css_property("font-size")
        campaign_price = driver.find_element(By.CSS_SELECTOR, "#box-product .information .campaign-price")
        campaign_price_font_size = campaign_price.value_of_css_property("font-size")

        product = {
            "name": driver.find_element(By.CSS_SELECTOR, "#box-product h1[itemprop='name']").get_attribute(
                "textContent"),
            "regular_price": {
                "value": regular_price.get_attribute("textContent"),
                "is_strikethrough": True if regular_price.tag_name == "s" else False,
                "is_grey": self.is_grey(regular_price.value_of_css_property("color")),
                "font_size": float(regular_price_font_size[:regular_price_font_size.find("px")])
            },
            "campaign_price": {
                "value": campaign_price.get_attribute("textContent"),
                "is_bold": True if campaign_price.tag_name == "strong" else False,
                "is_red": self.is_red(campaign_price.value_of_css_property("color")),
                "font_size": float(campaign_price_font_size[:campaign_price_font_size.find("px")])
            }
        }

        return product

    def test_product_name(self, driver, product_main_page, product_page):
        assert product_main_page["name"] == product_page["name"], \
            "Product name on the main page differs from the one on the product page."

    def test_product_prices(self, driver, product_main_page, product_page):
        try:
            assert product_main_page["regular_price"]["value"] == product_page["regular_price"]["value"]
        except AssertionError:
            print("Regular price on the main page differs from the one on the product page.")

        try:
            assert product_main_page["campaign_price"]["value"] == product_page["campaign_price"]["value"]
        except AssertionError:
            print("Campaign price on the main page differs from the one on the product page.")

    def test_regular_price_style(self, driver, product_main_page, product_page):
        try:
            assert product_main_page["regular_price"]["is_strikethrough"] and product_main_page["regular_price"]["is_grey"]
        except AssertionError:
            print("Regular price on the main page has unexpected style.")

        try:
            assert product_page["regular_price"]["is_strikethrough"] and product_page["regular_price"]["is_grey"]
        except AssertionError:
            print("Regular price on the product page has unexpected style.")

    def test_campaign_price_style(self, driver, product_main_page, product_page):
        try:
            assert product_main_page["campaign_price"]["is_bold"] and product_main_page["campaign_price"]["is_red"]
        except AssertionError:
            print("Campaign price on the main page has unexpected style.")

        try:
            assert product_page["campaign_price"]["is_bold"] and product_page["campaign_price"]["is_red"]
        except AssertionError:
            print("Campaign price on the product page has unexpected style.")

    def test_prices_fonts_sizes(self, driver, product_main_page, product_page):
        assert product_main_page["regular_price"]["font_size"] < product_main_page["campaign_price"]["font_size"], \
            "Font of regular price should be smaller than the one of campaign price on the main page."

        assert product_page["regular_price"]["font_size"] < product_page["campaign_price"]["font_size"],\
            "Font of regular price should be smaller than the one of campaign price on the product page."

    @staticmethod
    def is_grey(color):
        rgba = eval(color[color.find("(")+1:color.find(")")])
        return True if rgba[0] == rgba[1] and rgba[1] == rgba[2] else False

    @staticmethod
    def is_red(color):
        rgba = eval(color[color.find("(") + 1:color.find(")")])
        return True if rgba[1] == 0 and rgba[2] == 0 else False
