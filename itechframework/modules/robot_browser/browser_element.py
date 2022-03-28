from robot.api.logger import info, debug
from selenium.webdriver import ActionChains
from itechframework.configuration.constants import BROWSER_TYPE
from itechframework.modules.waitutils import waituntiltrue


class BrowserElement:
    def __init__(self, element, by, locator):
        from itechframework.modules.browser_manager.BrowserManager import BrowserManager

        self._browser = BrowserManager().get_browser(BROWSER_TYPE)
        self.element = element
        self.by = by
        self.locator = locator

    @classmethod
    def from_locator(cls, by, locator):
        from itechframework.modules.browser_manager.BrowserManager import BrowserManager

        browser = BrowserManager().get_browser(BROWSER_TYPE)
        return browser.find_element_or_raise(by, locator)

    @classmethod
    def find_elements(cls, by, locator):
        from itechframework.modules.browser_manager.BrowserManager import BrowserManager

        browser = BrowserManager().get_browser(BROWSER_TYPE)
        return [BrowserElement(e.element, by, locator) for e in browser.find_elements(by, locator)]

    def input_text(self, text):
        info(f'Sending {text!r} to {self.by!r} {self.locator!r}')
        self.element.send_keys(text)

    def click_element(self):
        debug(f'Clicking {self.by!r} {self.locator!r}')
        if self.is_clickable():
            self.log_screenshot()
            self.element.click()
        else:
            return False

    def move_to_element(self):
        debug(f'Moving to {self.by!r} {self.locator!r}')
        hover: ActionChains = ActionChains(self._browser.driver).move_to_element(self.element)
        hover.perform()

    def log_screenshot(self):
        info(f'<img src="data:image/png;base64, {self.element.screenshot_as_base64}">', html=True)

    @waituntiltrue
    def is_clickable(self):
        if self.element.is_displayed() and self.element.is_enabled():
            return True
