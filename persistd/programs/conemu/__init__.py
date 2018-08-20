import platform

from persistd.programs.conemu.conemu_windows import ConEmuWindows

_implementations = {
    'Windows': ConEmuWindows,
}

ConEmu = None
try:
    ConEmu = _implementations[platform.system()]
except KeyError:
    ConEmu = None

CODE_NAME = 'conemu'
HUMAN_READABLE_NAME = 'ConEmu'
PROGRAM_CLASS = ConEmu
