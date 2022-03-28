class BasePage:
    def __init__(self, browser) -> None:
        self.browser = browser
        self.url = browser.get_location

    @property
    def get_current_location(self):
        return self.url
