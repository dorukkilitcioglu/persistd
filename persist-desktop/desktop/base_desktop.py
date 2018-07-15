from abc import ABC, abstractmethod

from util.persistable import Persistable


class BaseDesktop(Persistable, ABC):

    def __init__(self, base_path, path):
        self.base_path = base_path
        self.path = path

    @abstractmethod
    def create_desktop(self):
        """ Creates a new desktop and saves the id to self
        """
        pass

    @abstractmethod
    def switch_to_desktop(self, desktop_id=None):
        """ Switches to the given desktop. If desktop_id
        is None, should switch to the created desktop.
        """
        pass

    @abstractmethod
    def close_desktop(self, desktop_id=None):
        """ Closes a given desktop. If desktop_id
        is None, should close the created desktop.
        """
        pass

    @abstractmethod
    def close_current_desktop(self):
        """ Closes the current desktop
        """
        pass

    @abstractmethod
    def launch_program(self, program_path, args=None, desktop_id=None):
        """ Launches a program, with optional args, at a given desktop.
        If desktop_id is None, should launch at the created desktop.
        """
        pass

    @property
    @abstractmethod
    def os(self):
        pass
