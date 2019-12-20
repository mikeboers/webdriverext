from selenium.common.exceptions import NoSuchElementException as _FindElementBase


class FindElementError(ValueError, _FindElementBase):

    """Easier name, and easier interface."""

    # Need to bring this back to "normal".
    def __str__(self):
        return self.args[0]

