from itechframework.modules.robot_browser.browser import Browser


class BasePage:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.url = self.browser.driver.current_url

    def save_screenshot(self, fname):
        self.browser.capture_page_screenshot(fname)
