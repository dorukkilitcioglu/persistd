import logging
import os
import shutil

import settings
from util.command_line import run_on_command_line
from util.savers import save_dict_to_json, load_dict_from_json

from programs.base_program import BaseProgram

logger = logging.getLogger(__name__)


class Chrome(BaseProgram):

    # The process id of Chrome window instance
    chrome_pid = None

    @property
    def object_persist_path(self):
        """ The path where this object will be persisted
        """
        return os.path.join(self.persist_path, 'chrome.json')

    def setup(self):
        """ Sets up the program for first use in this project.
        """
        pass

    def start(self):
        """ Starts a new instance of this program
        """
        pid = self.desktop.launch_program([settings.CHROME_PATH, "--new-window"], open_async=True, sleep=2)
        if pid is not None:
            logger.info("Started Chrome.")
            self.chrome_pid = pid
            return True
        else:
            logger.error("Could not start Chrome.")
            return False

    def close(self):
        """ Closes the program, persisting the state
        """
        return_code, _, _ = run_on_command_line(["taskkill", "-pid", str(self.chrome_pid)])
        if return_code is 0:
            logger.info("Closed Chrome window")
            self.conemu_pid = None
            return True
        else:
            logger.error("Could not close Chrome window")
            return False

    def destroy(self):
        """ Deletes all info regarding this program from the project
        """
        shutil.rmtree(self.persist_path)

    def save(self, path=None):
        """ Saves the variables to json
        """
        path = path or self.object_persist_path
        save_dict_to_json(self, path, ['desktop'])

    def load(self, path=None):
        """ Loads variables from json
        """
        path = path or self.object_persist_path
        load_dict_from_json(self, path)
