import platform

from programs.sublime_text.sublime_text_windows import SublimeTextWindows

_implementations = {
    'Windows': SublimeTextWindows,
}

SublimeText = None
try:
    SublimeText = _implementations[platform.system()]
except KeyError:
    SublimeText = None
