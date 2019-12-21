from urllib.parse import urlencode
import atexit
import base64 as b64
import datetime as dt
import os
import time
import weakref

from selenium.webdriver import Chrome as _Chrome, ChromeOptions

from .download import Download
from .error import JavascriptError
from .findelement import FindElementMixin
from .utils import call_until_true
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

        self._downloads = weakref.WeakValueDictionary()

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

    def set_download_filename(self, filename):
        self.execute_script('WebDriverExt.setDownloadFilename(arguments[0])', filename)

    def download(self, url, **options):
        options['url'] = url
        id_ = self.execute_async_chrome('downloads.download', options)
        try:
            obj = self._downloads[id_]
        except KeyError:
            obj = self._downloads[id_] = Download(self, id_)
        return obj

    def get_downloads(self, **query):
        
        wait = query.pop('wait', False)
        timeout = query.pop('timeout', 10)

        # Convert times to ms.
        for key, value in query.items():
            if isinstance(value, dt.datetime):
                query[key] = value.isoformat('T') #int(value.timestamp() * 1000)

        if wait:
            return call_until_true(self._get_downloads, kwargs=query, timeout=timeout) or []
        else:
            return self._get_downloads(**query)

    def _get_downloads(self, **query):

        ret = []

        for data in self.execute_async_chrome('downloads.search', query):
            id_ = data['id']
            try:
                obj = self._downloads[id_]
            except KeyError:
                obj = self._downloads[id_] = Download(self, id_)
            obj.data.update(data)
            ret.append(obj)
        return ret

    def get_download(self, **kwargs):
        ret = self.get_downloads(**kwargs)
        if len(ret) != 1:
            raise ValueError(f'found {len(ret)} downloads')
        return ret[0]




