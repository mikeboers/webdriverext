import functools
import time
import datetime

from .utils import call_until_true

class Download(object):

    def __init__(self, driver, id):

        self.driver = driver
        self.id = id
        self.data = {'state': 'in_progress'}

    @property
    def in_progress(self):
        return self.data['state'] == 'in_progress'
    @property
    def complete(self):
        return self.data['state'] == 'complete'
    @property
    def interrupted(self):
        return self.data['state'] == 'interrupted'

    def refresh(self, force=False):
        if force or self.in_progress:
            # This handles the update.
            res = self.driver.get_downloads(id=self.id)
            if len(res) != 1:
                raise ValueError("download does not exist")

    def get(self, name):
        self.refresh()
        return self.data[name]

    def __repr__(self):
        self.refresh()
        return '<webdriverext.Download #{id}: {fileSize} bytes {state} at {filename!r}>'.format(**self.data)

    def _make_property(name, timestamp=False):
        @property
        def _property(self):
            value = self.get(name)
            if value and timestamp:
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
            return value
        return _property

    by_extension_id = _make_property('byExtensionId')
    by_extension_name = _make_property('byExtensionName')
    bytes_received = _make_property('bytesReceived')
    can_resume = _make_property('canResume')
    danger = _make_property('danger')
    end_time = _make_property('end_time', timestamp=True)
    exists = _make_property('exists')
    file_size = _make_property('fileSize')
    filename = _make_property('filename')
    final_url = _make_property('finalUrl')
    incognito = _make_property('incognito')
    mime = _make_property('mime')
    paused = _make_property('paused')
    referrer = _make_property('referrer')
    start_time = _make_property('startTime', timestamp=True)
    state = _make_property('state')
    total_bytes = _make_property('totalBytes')
    url = _make_property('url')

    def wait(self, timeout=10):
        call_until_true(self.refresh, __key__=lambda _: not self.in_progress, __timeout__=timeout)
        return None if self.in_progress else self.complete

