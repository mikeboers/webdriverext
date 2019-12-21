import json
import time


def jprint(obj, indent=4, sort_keys=True):
    print(json.dumps(obj, indent=indent, sort_keys=sort_keys))



def call_until_true(func, *args, **kwargs):
    key = kwargs.pop('__key__', None)
    timeout = kwargs.pop('__timeout__', None)
    return call_until_true_ext(func, args, kwargs, key, timeout)

def call_until_true_ext(func, args, kwargs, key=None, timeout=10):

    key = key or (lambda x: bool(x))
    timeout = timeout or 10

    end = time.monotonic() + timeout
    delay = 0.1
    while True:

        obj = func(*args, **kwargs)
        if key(obj):
            return obj

        delay = min(delay, end - time.monotonic())
        if delay < 0:
            return

        time.sleep(delay)
        delay *= 2
