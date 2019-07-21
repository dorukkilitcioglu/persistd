import json
import os

from persistd.util.paths import CODE_PATH, SETTINGS_PATH
from persistd.util.savers import copy_file

DEFAULT_SETTINGS_PATH = os.path.join(CODE_PATH, 'settings', 'default.json')
LOCAL_SETTINGS_PATH = os.path.join(SETTINGS_PATH, 'local.json')

if not os.path.exists(LOCAL_SETTINGS_PATH):
    copy_file(DEFAULT_SETTINGS_PATH, LOCAL_SETTINGS_PATH)

BASE_PATH = None
SUBLIME_TEXT_PATH = None
CONEMU_PATH = None
CHROME_PATH = None

with open(os.path.join(DEFAULT_SETTINGS_PATH), 'r') as fp:
    settings = json.load(fp)
    BASE_PATH = settings['BASE_PATH']
    SUBLIME_TEXT_PATH = settings['SUBLIME_TEXT_PATH']
    CONEMU_PATH = settings['CONEMU_PATH']
    CHROME_PATH = settings['CHROME_PATH']

with open(os.path.join(LOCAL_SETTINGS_PATH), 'r') as fp:
    settings = json.load(fp)
    if 'BASE_PATH' in settings:
        BASE_PATH = settings['BASE_PATH']
    if 'SUBLIME_TEXT_PATH' in settings:
        SUBLIME_TEXT_PATH = settings['SUBLIME_TEXT_PATH']
    if 'CONEMU_PATH' in settings:
        CONEMU_PATH = settings['CONEMU_PATH']
    if 'CHROME_PATH' in settings:
        CHROME_PATH = settings['CHROME_PATH']
