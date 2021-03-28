import os
import logging
import shutil

from persistd.programs.base_program import BaseProgram
from persistd.settings import settings
from persistd.util.command_line import run_on_command_line
from persistd.util.savers import save_dict_to_json, load_dict_from_json

logger = logging.getLogger(__name__)


class VSCodeWindows(BaseProgram):
    vscode_pid = None
    full_path = None
    is_remote = False

    @property
    def object_persist_path(self):
        """ The path where this object will be persisted
        """
        return os.path.join(self.persist_path, 'vscode.json')

    def setup(self):
        """ Sets up the program for first use in this project.
        """
        # Nothing to do
        pass

    def start(self):
        """ Starts a new instance of this program
        """
        program_args = [settings.VSCODE_PATH, "-n"]
        if self.is_remote:
            program_args.append("--folder_uri")
        program_args.append(self.full_path if self.full_path else self.project_path)
        print(program_args)
        print(os.environ)
        pid = self.desktop.launch_program(program_args, open_async=True)
        if pid is not None:
            logger.info("Started VSCode.")
            self.vscode_pid = pid
            return True
        else:
            logger.error("Could not start VSCode.")
            return False

    def persist(self):
        """ Persists the state without closing
        """
        # Nothing to do for now
        return True

    def close(self):
        """ Closes the program, persisting the state
        """
        return_code, _, _ = run_on_command_line(["taskkill", "-pid", str(self.vscode_pid)])
        if return_code is 0:
            logger.info("Closed VSCode window")
            self.vscode_pid = None
            return True
        else:
            logger.error("Could not close VSCode window")
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
