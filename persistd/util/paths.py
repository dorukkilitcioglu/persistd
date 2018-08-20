import os


def _get_persistd_path():
    """ Gets the path to base persistd folder
    """
    return os.path.abspath(os.path.join(__file__, '..', '..'))


# Path to the base persistd folder.
PERSISTD_PATH = _get_persistd_path()

# Path to the programs folder
PROGRAMS_PATH = os.path.join(PERSISTD_PATH, 'programs')

# Path to desktops folder
DESKTOPS_PATH = os.path.join(PERSISTD_PATH, 'desktops')
