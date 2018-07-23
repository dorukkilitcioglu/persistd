from abc import ABC, abstractmethod


class Persistable(ABC):

    @abstractmethod
    def save(self, path=None):
        """ Saves the current object to file path. If path is None,
        should save to self.path.
        """
        pass

    @abstractmethod
    def load(self, path=None):
        """ Loads the current object from file path. If path is None,
        should load from self.path.
        """
        pass
