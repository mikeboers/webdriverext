from urllib.parse import urlencode
import atexit
import base64 as b64
import os
import time

from selenium.webdriver import Chrome as _Chrome, ChromeOptions

from .error import JavascriptError
from .findelement import FindElementMixin
from .webelement import WebElement


class Chrome(FindElementMixin, _Chrome):

    _web_element_cls = WebElement

    def __init__(self, *args, **kwargs):

        options = kwargs.setdefault('options', ChromeOptions())
        options.add_argument('load-extension={}'.format(os.path.abspath(os.path.join(
            __file__, '..', 'webext'
        ))))

        navigator_webdriver = kwargs.pop('navigator_webdriver', True)

        super().__init__(*args, **kwargs)

        # TODO: Put this behind a flag or something.
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

    def __del__(self):
        self.quit()

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

    def execute_async_chrome(self, name, *args):
        """Call a function from the webext API.
    
        :param str name: Dotted string name of function to call under ``chrome``
            object, e.g. ``cookies.getAll``.

        Remaining arguments are passed to the function.

        This assumes that the last argument to the function is a callback for
        the result, which is required for the operation of this function.

        """
        res = self.execute_async_script('WebDriverExt.chrome.apply(null, arguments)', name, *args)
        if res.get('error'):
            raise JavascriptError(res['error'])
        return res['result']

    def get_cookies(self, **details):
        """Get cookies for the given URL.
    
        .. seealso:: https://developer.chrome.com/extensions/cookies#method-getAll

        """
        return self.execute_async_chrome('cookies.getAll', details)

    def download(self, url, **options):
        options['url'] = url
        return self.execute_async_chrome('downloads.download', options)

    def get_downloads(self, **query):
        return self.execute_async_chrome('downloads.search', query)
