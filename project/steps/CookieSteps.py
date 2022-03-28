import os
import pathlib
import pickle
from logging import info

from robot.api.deco import keyword
from selenium.common.exceptions import TimeoutException

from itechframework.modules.robot_browser.browser import Browser
from configuration.constants import WIKI_URL, COOKIES_PATH
from project.page_objects.wiki_main_page import WikiMainPage

file_path = pathlib.Path(COOKIES_PATH, "cookies.json")


class CookieSteps:
    @staticmethod
    @keyword(name="Open Wiki")
    def open_wiki(browser: Browser):
        browser.go_to(WIKI_URL)
        return WikiMainPage(browser)

    @staticmethod
    @keyword(name="Login To Wiki")
    def login_to_wiki(page: WikiMainPage, login, password):
        try:
            page.get_login_fields()
            page.login_input.input_text(login)
            page.password_input.input_text(password)
            page.remember_me.click_element()
            page.submit_button.click_element()
            page.browser.wait_until_visible('xpath', WikiMainPage.ATLASSIAN_LOGO_LOCATOR)
        except TimeoutException:
            info(f'User has already logged in!')

    @staticmethod
    @keyword(name="Save Cookies")
    def save_cookies(browser: Browser):
        if not pathlib.Path(COOKIES_PATH).exists():
            os.mkdir(pathlib.Path(COOKIES_PATH))
        browser.save_cookies(file_path)

    @staticmethod
    @keyword(name="Load Cookies")
    def load_cookies(browser):
        browser.load_cookies(file_path)
        browser.go_to(browser.get_location())

    @staticmethod
    @keyword(name="Check If Logged In")
    def check_if_logged_in(browser):
        browser.find_element_or_raise('xpath', '//*[@id="login-container"]/*//a[contains(@href, "dashboard.action")]')
