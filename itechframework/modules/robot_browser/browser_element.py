from robot.api.logger import info, debug, warn
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

from itechframework.configuration.constants import BROWSER_TYPE
from itechframework.modules.waitutils import waituntiltrue


def updateifstale(func, max_attempts=5):
    def wrapper(self, *args, **kwargs):
        attempt = 1
        while True:
            try:
                func(self, *args, **kwargs)
            except StaleElementReferenceException:
                warn(f'Tried to interact with stale element {self.by!r} {self.locator!r}! Updating...')
                if attempt >= max_attempts:
                    raise Exception(f'Maximum number of tries reached for {self.by!r} {self.locator!r}!')
                self.update_element()
                attempt += 1
                continue
            return func

    return wrapper


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

    @updateifstale
    def input_text(self, text):
        info(f'Sending {text!r} to {self.by!r} {self.locator!r}')
        self.element.send_keys(text)

    @updateifstale
    def click_element(self, max_attempts=5):
        debug(f'Clicking {self.by!r} {self.locator!r}')
        if self.wait_clickable():
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
    def wait_clickable(self):
        if self.element.is_displayed() and self.element.is_enabled():
            return True

    def update_element(self):
        self.element = BrowserElement.from_locator(self.by, self.locator).element
