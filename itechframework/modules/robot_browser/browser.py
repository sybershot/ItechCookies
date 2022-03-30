import json
import pickle
from typing import List
from robot.api.deco import keyword
from robot.api.logger import info, debug
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from itechframework.configuration.constants import TIMEOUT
from itechframework.modules.robot_browser.browser_element import BrowserElement


class Browser:
    def __init__(self, driver, name):
        self.driver: WebDriver = driver
        self.name = name

    @keyword(name='Close browser')
    def close_browser(self):
        self.driver.quit()

    @keyword(name='Get location')
    def get_location(self):
        return self.driver.current_url

    @keyword(name='Go to')
    def go_to(self, url):
        info(f'Loading {url}')
        self.driver.get(url)

    @keyword(name='Wait until visible')
    def wait_until_visible(self, by, locator, timeout=TIMEOUT):
        info(f'Waiting until {by!r} {locator!r} is visible')
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))

    @keyword(name='Capture page screenshot')
    def capture_page_screenshot(self, file_name):
        image_path = file_name + '.png'
        self.driver.save_screenshot(image_path)
        info(f'<img src="{image_path}">', html=True)

    def find_elements(self, by, locator) -> List[BrowserElement]:
        info(f'Searching all elements by {by!r} {locator!r}')
        return [BrowserElement(e, by, locator) for e in self.driver.find_elements(by, locator)]

    def find_element_or_raise(self, by, locator, timeout=TIMEOUT) -> BrowserElement:
        debug(f'Searching element {by!r} {locator!r}')
        if element := WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, locator))):
            return BrowserElement(element, by, locator)
        else:
            raise NoSuchElementException(f'Failed to find element {by!r} {locator!r}!')

    def is_exist(self, by, locator):
        try:
            self.driver.find_element(by, locator)
        except NoSuchElementException:
            return False
        return True

    def save_cookies(self, file_path):
        cookies = self.driver.get_cookies()
        with open(file_path, 'w', newline='') as cookiestream:
            json.dump(cookies, cookiestream)

    def load_cookies(self, file_path):
        with open(file_path, 'r', newline='') as cookieloader:
            cookies = json.load(cookieloader)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
