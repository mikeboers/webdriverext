from urllib.parse import urlencode
import atexit
import base64 as b64
import os
import time

from selenium.webdriver import Chrome as _Chrome, ChromeOptions

from .webelement import WebElement
from .findelement import FindElementMixin


class Chrome(FindElementMixin, _Chrome):

    _web_element_cls = WebElement

    def __init__(self, *args, **kwargs):

        options = kwargs.setdefault('options', ChromeOptions())
        options.add_argument('load-extension={}'.format(os.path.abspath(os.path.join(
            __file__, '..', 'webext'
        ))))

        navigator_webdriver = kwargs.pop('navigator_webdriver', True)

        super().__init__(*args, **kwargs)

        atexit.register(self.quit)
        
        # Disable navigator.webdriver, which breaks a LOT of sites.
        if not navigator_webdriver:
            self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })

    def xhr(self, method, url, data=None):

        if data is not None and not isinstance(data, str):
            data = urlencode(data)

        return self.execute_script(
            '''
                let [method, url, data] = arguments
                var req = new XMLHttpRequest()
                req.open(method, url, false) // false -> sync
                req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
                req.send(data)
                return req.responseText
            ''',
            method,
            url,
            data,
        )

    def post(self, url, data=None):
        return self.xhr('POST', url, data)

    def get_cookies(self, url=None):
        pass
