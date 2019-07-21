import os
import sys

from persistd.settings.default import *
from persistd.util.paths import CODE_PATH, SETTINGS_PATH
from persistd.util.savers import copy_file

DEFAULT_SETTINGS_PATH = os.path.join(CODE_PATH, 'settings', 'default.py')
LOCAL_SETTINGS_PATH = os.path.join(SETTINGS_PATH, 'local.py')

if not os.path.exists(LOCAL_SETTINGS_PATH):
    copy_file(DEFAULT_SETTINGS_PATH, LOCAL_SETTINGS_PATH)

sys.path.append(os.path.dirname(LOCAL_SETTINGS_PATH))

from local import *
