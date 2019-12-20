import json


def jprint(obj, indent=4, sort_keys=True):
    print(json.dumps(obj, indent=indent, sort_keys=sort_keys))

