import json
import os

from persistd.util.paths import CODE_PATH, SETTINGS_PATH
from persistd.util.savers import copy_file

DEFAULT_SETTINGS_PATH = os.path.join(CODE_PATH, 'settings', 'default.json')
LOCAL_SETTINGS_PATH = os.path.join(SETTINGS_PATH, 'local.json')

if not os.path.exists(LOCAL_SETTINGS_PATH):
    copy_file(DEFAULT_SETTINGS_PATH, LOCAL_SETTINGS_PATH)


# source: https://goodcode.io/articles/python-dict-object/
class attrdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value
        with open(LOCAL_SETTINGS_PATH, 'w') as fp:
            json.dump(self, fp)

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


settings = attrdict()

with open(DEFAULT_SETTINGS_PATH, 'r') as fp:
    default_settings = json.load(fp)
    settings.update(default_settings)

with open(LOCAL_SETTINGS_PATH, 'r') as fp:
    local_settings = json.load(fp)
    settings.update(local_settings)
