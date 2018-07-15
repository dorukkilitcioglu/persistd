from abc import ABC, abstractmethod

from util.persistable import Persistable


class BaseProgram(Persistable, ABC):

    def __init__(self, base_path, path):
        self.base_path = base_path
        self.path = path

    @abstractmethod
    def start(self):
        """ Starts a brand new instance of this program
        """
        pass

    @abstractmethod
    def restart(self):
        """ Restarts the program from where it was left
        """
        pass

    @abstractmethod
    def close(self):
        """ Closes the program, persisting the state
        """
        pass
