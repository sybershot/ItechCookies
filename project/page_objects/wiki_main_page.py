from itechframework.modules.robot_browser.browser_element import BrowserElement
from project.page_objects.base_page import BasePage


class WikiMainPage(BasePage):
    LOGIN_INPUT_LOCATOR = '//input[@id="os_username"]'
    PASSWORD_INPUT_LOCATOR = '//input[@id="os_password"]'
    SUBMIT_BUTTON_LOCATOR = '//input[@id="loginButton"]'
    ATLASSIAN_LOGO_LOCATOR = '//div/a[@rel="nofollow"]'
    REMEMBER_ME_LOCATOR = '//label[@for="os_cookie"]'

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.login_input = None
        self.password_input = None
        self.submit_button = None
        self.remember_me = None

    def get_login_fields(self):
        self.login_input = BrowserElement.from_locator('xpath', self.LOGIN_INPUT_LOCATOR)
        self.password_input = BrowserElement.from_locator('xpath', self.PASSWORD_INPUT_LOCATOR)
        self.submit_button = BrowserElement.from_locator('xpath', self.SUBMIT_BUTTON_LOCATOR)
        self.remember_me = BrowserElement.from_locator('xpath', self.REMEMBER_ME_LOCATOR)

