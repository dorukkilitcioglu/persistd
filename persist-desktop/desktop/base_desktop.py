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
    def launch_program(self, program_path, args=None, desktop_id=None, open_async=False, sleep=None):
        """ Launches a program, with optional args, at a given desktop.

        Args:
            command::list(str)
                The command to run. The first element in list is the
                executable, the rest are the arguments
            input::bytes
                The input to be fed in as STDIN
            desktop_id::int
                The desktop to launch in. If None, should launch at
                the created desktop
            open_async::bool
                Whether to open the process as asynchronous. If set,
                there will not be any communication through stdin and
                stdout, and the return code may not be set.
            sleep::float
                The amount of time to sleep before moving the process

        Returns:
            pid::int
                The process id of the created process. May be None
                if the process was not successfully launched..
        """
        pass

    @property
    @abstractmethod
    def os(self):
        pass
