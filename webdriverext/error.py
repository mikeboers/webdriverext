from selenium.common.exceptions import (
    NoSuchElementException as _FindElementBase,
    JavascriptException as _JavascriptError,
)

class FindElementError(ValueError, _FindElementBase):

    """Easier name, and easier interface."""

    # Need to bring this back to "normal".
    def __str__(self):
        return self.args[0]

class JavascriptError(ValueError, _JavascriptError):

    """Easier name, and easier interface."""

    # Need to bring this back to "normal".
    def __str__(self):
        return self.args[0]
