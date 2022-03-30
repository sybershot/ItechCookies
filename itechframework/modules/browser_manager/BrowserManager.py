from robot.api.deco import keyword

from itechframework.modules.robot_browser.meta_singleton import MetaSingleton
from itechframework.modules.robot_browser.browser import Browser
from driver_factory import DriverFactory


class BrowserManager(metaclass=MetaSingleton):

    def __init__(self):
        self.browsers = {}

    @keyword('Get Browser')
    def get_browser(self, browser_type):
        if browser := self.browsers.get(browser_type, None):
            return browser
        browser = Browser(DriverFactory.get_driver(browser_type), browser_type)
        self.browsers[browser_type] = browser
        return browser

    @keyword('Close browser')
    def close_browser(self, browser):
        if browser.name not in self.browsers:
            raise Exception("Tried to close unknown/unregistered browser")
        self.browsers.pop(browser.name)
        browser.close_browser()
