import logging

from util.command_line import run_on_command_line

from program.base_program import BaseProgram
import settings

logger = logging.getLogger(__name__)


class SublimeText(BaseProgram):

    def start(self):
        """ Starts a brand new instance of SublimeText
        """
        return_code, _, _ = run_on_command_line([settings.SUBLIME_TEXT_PATH, self.base_path])
        if return_code is 0:
            logger.info("Started SublimeText on path %s", self.base_path)
            return True
        else:
            logger.error("Could not start SublimeText on path %s", self.base_path)
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


        Here, we implement #2. #3 is probably a better solution over the long run.
        """
        return_code, _, _ = run_on_command_line([settings.SUBLIME_TEXT_PATH, "--command", "close_window"])
        if return_code is 0:
            logger.info("Closed SublimeText window")
            return True
        else:
            logger.error("Could not close SublimeText window")
            return False

    def save(self, path=None):
        """ Nothing to persist except for the folder path
        """
        pass

    def load(self, path=None):
        """ Nothing to persist except for the folder path
        """
        pass
