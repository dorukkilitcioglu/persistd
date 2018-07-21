import os


def _get_persist_desktop_path():
    """ Gets the path to base persist-desktop folder
    """
    return os.path.abspath(os.path.join(__file__, '..', '..'))


# Path to the base persist-desktop folder.
PERSIST_DESKTOP_PATH = _get_persist_desktop_path()

# Path to the programs folder
PROGRAMS_PATH = os.path.join(PERSIST_DESKTOP_PATH, 'programs')
