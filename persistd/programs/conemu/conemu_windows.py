import logging
import os
import shutil

import persistd.settings as settings
from persistd.util.command_line import run_on_command_line
from persistd.util.paths import PROGRAMS_PATH
from persistd.util.savers import copy_file, save_dict_to_json, load_dict_from_json

from persistd.programs.base_program import BaseProgram

logger = logging.getLogger(__name__)


class ConEmuWindows(BaseProgram):

    # The process id of ConEmu instance
    conemu_pid = None

    @property
    def startfile_filename(self):
        """ Filename of the startfile
        """
        return '%s_startfile.txt' % self.project_name

    @property
    def startfile_path(self):
        """ Path of the startfile
        """
        return os.path.join(self.persist_path, self.startfile_filename)

    @property
    def object_persist_path(self):
        """ The path where this object will be persisted
        """
        return os.path.join(self.persist_path, 'conemu.json')

    def setup(self):
        """ Sets up the program for first use in this project.
        """
        default_startfile_path = os.path.join(PROGRAMS_PATH, 'conemu', 'startfile_windows.txt')
        copy_file(default_startfile_path, self.startfile_path)

    def start(self):
        """ Starts a new instance of this program
        """
        pid = self.desktop.launch_program([settings.CONEMU_PATH, "/cmd", "@%s" % self.startfile_path], open_async=True)
        if pid is not None:
            logger.info("Started ConEmu.")
            self.conemu_pid = pid
            return True
        else:
            logger.error("Could not start ConEmu.")
            return False

    def close(self):
        """ Closes the program, persisting the state
        """
        return_code, _, _ = run_on_command_line(["taskkill", "-pid", str(self.conemu_pid)])
        if return_code is 0:
            logger.info("Closed ConEmu window")
            self.conemu_pid = None
            return True
        else:
            logger.error("Could not close ConEmu window")
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
