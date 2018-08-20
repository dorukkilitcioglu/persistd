import platform

from persistd.programs.sublime_text.sublime_text_windows import SublimeTextWindows

_implementations = {
    'Windows': SublimeTextWindows,
}

SublimeText = None
try:
    SublimeText = _implementations[platform.system()]
except KeyError:
    SublimeText = None

CODE_NAME = 'sublime_text'
HUMAN_READABLE_NAME = 'Sublime Text'
PROGRAM_CLASS = SublimeText
