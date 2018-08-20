import logging
import os
import shutil

import persistd.settings as settings
from persistd.util.command_line import run_on_command_line
from persistd.util.savers import save_dict_to_json, load_dict_from_json

from persistd.programs.base_program import BaseProgram

logger = logging.getLogger(__name__)

BASE_URL = "http://idontthinkthis.domainwilleverexist?project_name=%s&action=%s"


class Chrome(BaseProgram):

    @property
    def object_persist_path(self):
        """ The path where this object will be persisted
        """
        return os.path.join(self.persist_path, 'chrome.json')

    def setup(self):
        """ Sets up the program for first use in this project.
        """
        warnings = ("\nWARNING:\n"
                    "Before running the project, make sure you install the Chrome extension\n"
                    "The instructions can be found at: https://github.com/dorukkilitcioglu/persistd#getting-started\n"
                    )
        print(warnings)

    def get_url(self, action):
        return BASE_URL % (self.project_name, action)

    def start(self):
        """ Starts a new instance of this program
        """
        pid = self.desktop.launch_program([settings.CHROME_PATH, "--new-window", self.get_url('start')], open_async=True, sleep=2, max_tries=0)
        if pid is not None:
            logger.info("Started Chrome.")
            return True
        else:
            logger.error("Could not start Chrome.")
            return False

    def close(self):
        """ Closes the program, persisting the state
        """
        return_code, _, _ = run_on_command_line([settings.CHROME_PATH, "--new-window", self.get_url('close')])
        if return_code is 0:
            logger.info("Closed Chrome window")
            return True
        else:
            logger.error("Could not close Chrome window")
            return False

    def destroy(self):
        """ Deletes all info regarding this program from the project
        """
        shutil.rmtree(self.persist_path)
        return_code, _, _ = run_on_command_line([settings.CHROME_PATH, "--new-window", self.get_url('destroy')])
        if return_code is 0:
            logger.info("Destroyed Chrome storage for this project")
            return True
        else:
            logger.error("Could not destroy Chrome storage for this project")
            return False

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
