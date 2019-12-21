from selenium.webdriver.remote.webelement import WebElement as _WebElement

from .findelement import FindElementMixin


class WebElement(FindElementMixin, _WebElement):

    def set_property(self, name, value):
        self.parent.execute_script('arguments[0][arguments[1]] = arguments[2]', self, name, value)
    

