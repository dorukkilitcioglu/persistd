import logging
import os

from util.command_line import run_on_command_line, kill_mutant
from util.paths import PROGRAMS_PATH
from util.savers import copy_file, save_dict_to_json, load_dict_from_json

from programs.base_program import BaseProgram
import settings

logger = logging.getLogger(__name__)


class SublimeTextWindows(BaseProgram):

    # The process id of the SublimeText instance
    sublime_pid = None

    @property
    def sublimeproj_filename(self):
        """ Filename of the sublime-project file
        """
        return '%s.sublime-project' % self.project_name

    @property
    def sublimeproj_path(self):
        """ Path of the sublime-project file
        """
        return os.path.join(self.persist_path, self.sublimeproj_filename)

    @property
    def sublime_exe_filename(self):
        """ Filename of the copied SublimeText executable
        """
        return 'sublime_text_%s.exe' % self.project_name

    @property
    def sublime_exe_path(self):
        """ Path of the copied SublimeText executable
        """
        standard_exe_path = settings.SUBLIME_TEXT_PATH
        return os.path.join(os.path.dirname(standard_exe_path), self.sublime_exe_filename)

    @property
    def object_persist_path(self):
        """ The path where this object will be persisted
        """
        return os.path.join(self.persist_path, 'sublime_text.json')

    def _kill_mutant(self):
        kill_mutant(process_name='sublime_text.exe', object_name='Sublime')

    def setup(self):
        """ Sets up the Sublime Text project
        """
        default_proj_path = os.path.join(PROGRAMS_PATH, 'sublime_text', 'default.sublime-project')
        copy_file(default_proj_path, self.sublimeproj_path)
        copy_file(settings.SUBLIME_TEXT_PATH, self.sublime_exe_path)

    def start(self):
        """ Starts a brand new instance of SublimeText
        """
        # TODO make this more deterministic
        # It seems like you need some waiting before switching sublimetext
        # So just sleep for 2 secs
        pid = self.desktop.launch_program([self.sublime_exe_path, self.project_path, "--project", self.sublimeproj_path], open_async=True, sleep=2)
        if pid is not None:
            logger.info("Started SublimeText on path %s", self.project_path)
            self.sublime_pid = pid
            return True
        else:
            logger.error("Could not start SublimeText on path %s", self.project_path)
            return False

    def restart(self):
        """ Restarts SublimeText from where it was left.
        """
        return self.start()

    def close(self):
        """ Closes the program, persisting the state

        Couple of ideas on how to do this with Sublime Text

         1:
            use "--wait" to let sublime hang the current command line
            use & to force it back and get pid
            use pid to kill it

            http://docs.sublimetext.info/en/latest/command_line/command_line.html
        2:
            "C:\\Program Files\\Sublime Text 3\\subl.exe" --command close_window
            use "--command" with "close_window" to close the active window
            http://docs.sublimetext.info/en/latest/reference/commands.html
        3:
            write custom plugin
            http://sublimetexttips.com/execute-a-command-every-time-sublime-launches/
            https://www.sublimetext.com/docs/3/api_reference.html#sublime.Window


        Here, we implement #1. #3 is probably a better solution over the long run.
        """
        return_code, _, _ = run_on_command_line(["taskkill", "-pid", str(self.sublime_pid)])
        if return_code is 0:
            logger.info("Closed SublimeText window")
            self.sublime_pid = None
            return True
        else:
            logger.error("Could not close SublimeText window")
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
