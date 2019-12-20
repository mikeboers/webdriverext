from selenium.webdriver.remote.webelement import WebElement as _WebElement

from .findelement import FindElementMixin


class WebElement(FindElementMixin, _WebElement):
    pass

