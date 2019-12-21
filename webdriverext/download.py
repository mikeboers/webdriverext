import functools
import time


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

    by_extension_id = property(lambda self: self.get('byExtensionId'))
    by_extension_name = property(lambda self: self.get('byExtensionName'))
    bytes_received = property(lambda self: self.get('bytesReceived'))
    can_resume = property(lambda self: self.get('canResume'))
    danger = property(lambda self: self.get('danger'))
    end_time = property(lambda self: self.get('endTime'))
    exists = property(lambda self: self.get('exists'))
    file_size = property(lambda self: self.get('fileSize'))
    filename = property(lambda self: self.get('filename'))
    final_url = property(lambda self: self.get('finalUrl'))
    incognito = property(lambda self: self.get('incognito'))
    mime = property(lambda self: self.get('mime'))
    paused = property(lambda self: self.get('paused'))
    referrer = property(lambda self: self.get('referrer'))
    start_time = property(lambda self: self.get('startTime'))
    state = property(lambda self: self.get('state'))
    total_bytes = property(lambda self: self.get('totalBytes'))
    url = property(lambda self: self.get('url'))

    def wait(self, timeout=10):
        end = time.monotonic() + timeout
        delay = 0.1
        while self.in_progress:
            delay = min(delay, end - time.monotonic())
            if delay < 0:
                break
            time.sleep(delay)
            self.refresh()
        return self.complete

