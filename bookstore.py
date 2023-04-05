import pathlib

from applitools.common import MatchLevel
from selenium import webdriver
from applitools.selenium import Eyes
from assertpy import assert_that
from selenium.webdriver.common.by import By

APPLITOOLS_API_KEY = '2XuawH46jX3b6w3S98tJrifUMJ107OJopnQI8AAbmL106dTY110'
APP_NAME = 'automation_bookstore'
APP_UNDER_TEST = 'https://automationbookstore.dev/'


class ForYourEyesOnly:
    def __init__(self):

        # if the web drivers are defined in the system environment path then use this
        # self.driver = webdriver.Chrome()

        # Assume the web drivers are embedded in code ('drivers' folder)
        if __debug__:
            self.driver = webdriver.Chrome(
                'C:\\Users\\AlfredoNatividad\\PycharmProjects\\ForYourEyesOnly\\drivers\\chromedriver.exe')
        else:
            self.driver = webdriver.Chrome(str(pathlib.Path().resolve()) + "\\drivers\\chromedriver.exe")
        self.driver.get(APP_UNDER_TEST)
        self.eyes = Eyes()

        # The API key is available in applitools eyes website under User->My API key
        self.eyes.api_key = APPLITOOLS_API_KEY

    def filter_books(self, search_text):
        element = self.driver.find_element(By.ID, 'searchBar')
        element.send_keys(search_text)

    def verify_visible_books_by_title(self, expected_title):
        elements = self.driver.find_elements(By.CSS_SELECTOR, '#productList li a h2')
        for element in elements:
            if expected_title in element.text:
                return True
        return False

    def test_filter_book(self):
        self.filter_books('Agile')
        result = self.verify_visible_books_by_title('Agile Testing')
        assert_that(result).is_equal_to(True)

    def close_my_eyes(self):
        self.driver.quit()
        self.eyes.close()

    def validate_window(self, tag=None):
        # self.eyes.open(self.driver, APP_NAME, test_name=self.get_test_name())
        self.eyes.open(self.driver, APP_NAME, test_name=APP_NAME)
        self.eyes.match_level = MatchLevel.LAYOUT
        self.eyes.check_window(tag=tag)

