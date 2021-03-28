import platform

from persistd.programs.vscode.vscode_windows import VSCodeWindows

_implementations = {
    'Windows': VSCodeWindows,
}

VSCode = None
try:
    VSCode = _implementations[platform.system()]
except KeyError:
    VSCode = None

CODE_NAME = 'vscode'
HUMAN_READABLE_NAME = 'VSCode'
PROGRAM_CLASS = VSCode
