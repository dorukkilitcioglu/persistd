from io import BytesIO
import logging
import os
import platform
import requests
from shutil import rmtree
import time
from zipfile import ZipFile

from persistd.util.command_line import run_on_command_line
from persistd.util.paths import DESKTOPS_PATH
from persistd.util.savers import save_dict_to_json, load_dict_from_json

from persistd.desktops.base_desktop import BaseDesktop

logger = logging.getLogger(__name__)


class VirtualDesktop(BaseDesktop):

    # ID of the currently used virtual desktop
    # Note that this may change if another desktop is
    # closed
    virtual_desktop_id = None

    @property
    def exe_path(self):
        # Path to VirtualDesktop.exe
        return os.path.join(DESKTOPS_PATH, 'VirtualDesktop.exe')

    @property
    def object_persist_path(self):
        """ The path where this object will be persisted
        """
        return os.path.join(self.persist_path, 'virtual_desktop.json')

    @property
    def os(self):
        return ('Windows', '10')

    def setup(self):
        if not os.path.exists(self.exe_path):
            return self._setup()
        return True

    def _setup(self):
        logger.info("Downloading VirtualDesktop from Github...")
        package_url = 'https://github.com/MScholtes/VirtualDesktop/archive/11597438e9559cbe19ef2927451129adfe6a6704.zip'
        zip_raw = requests.get(package_url)

        zip_path = os.path.join(DESKTOPS_PATH, 'VirtualDesktop')
        logger.info("Extracting VirtualDesktop contents to %s", zip_path)
        zip_bytes = BytesIO(zip_raw.content)
        zip_file = ZipFile(zip_bytes)
        zip_file.extractall(zip_path)

        logger.info("Installing VirtualDesktop...")
        install_dir = os.path.join(zip_path, 'VirtualDesktop-11597438e9559cbe19ef2927451129adfe6a6704')
        cwd = os.getcwd()
        os.chdir(install_dir)
        return_code, stdout, _ = run_on_command_line(['Compile.bat'], input='.'.encode('utf-8'))
        os.chdir(cwd)
        if return_code is 0:
            logger.info("Successfully installed VirtualDesktop!")
        else:
            logger.error("Could not install VirtualDesktop! Error: %s", str(stdout))
            return False

        logger.info("Cleaning up VirtualDesktop installation files...")
        os.rename(os.path.join(install_dir, 'VirtualDesktop.exe'), self.exe_path)
        rmtree(zip_path)

        logger.info("VirtualDesktop is ready to go!")
        return True

    def create_desktop(self):
        """ Creates a new desktop and saves the id to self

        Returns:
            success::bool
                Whether a new virtual desktop was created
        """
        return_code, stdout, _ = run_on_command_line([self.exe_path, "-new"])
        # TODO find a better way to do this
        # return_code is the new desktop id no matter if it succeeded or not
        if "error" not in stdout:
            self.virtual_desktop_id = return_code
            logger.info("Created virtual desktop #%s", self.virtual_desktop_id)
            return True
        else:
            logger.error("Could not create virtual desktop")
            return False

    def switch_to_desktop(self, desktop_id=None):
        """ Switches to the given desktop. If desktop_id
        is None, should switch to the created desktop.
        """
        desktop_id = desktop_id if desktop_id is not None else self.virtual_desktop_id
        return_code, stdout, _ = run_on_command_line([self.exe_path, '-Switch:%s' % desktop_id])
        if return_code is desktop_id:
            logger.info("Switched to virtual desktop #%s", desktop_id)
            return True
        else:
            logger.error("Could not switch to virtual desktop #%s", desktop_id)
            return False

    def close_desktop(self, desktop_id=None):
        """ Closes a given desktop. If desktop_id
        is None, should close the created desktop.
        """
        desktop_id = desktop_id if desktop_id is not None else self.virtual_desktop_id
        return_code, stdout, _ = run_on_command_line([self.exe_path, '-Remove:%s' % desktop_id])
        if return_code is desktop_id:
            logger.info("Removed virtual desktop #%s", desktop_id)
            return True
        else:
            logger.error("Could not remove virtual desktop #%s", desktop_id)
            return False

    def close_current_desktop(self):
        """ Closes the current desktop
        """
        return_code, stdout, _ = run_on_command_line([self.exe_path, '-GetCurrentDesktop', '-Remove'])
        # TODO find a better way to do this
        # return_code is the current desktop id no matter if it succeeded or not
        if "error" not in stdout:
            logger.info("Removed current virtual desktop")
            return True
        else:
            logger.error("Could not remove current virtual desktop")
            return False

    def move_program(self, pid, desktop_id=None, max_tries=3, sleep=None):
        """ Moves a program to a given desktop using its process id.

        Args:
            pid::int
                The process id
            desktop_id::int
                The desktop to launch in. If None, should launch at
                the created desktop
            max_tries::int
                The max # of times this action should be tried
            sleep::float
                The amount of time to sleep before moving the process

        Returns:
            pid::int
                The process id of the created process. May be None
                if the process was not successfully launched.
        """
        desktop_id = desktop_id if desktop_id is not None else self.virtual_desktop_id
        return_code = -1
        counter = 0
        while return_code != self.virtual_desktop_id and counter < max_tries:
            return_code, stdout, _ = run_on_command_line([self.exe_path, '-GetDesktop:%s' % desktop_id, '-MoveWindow:%d' % pid])
            if return_code is self.virtual_desktop_id:
                logger.info("Moved program (pid=%d) to virtual desktop %s successfully.", pid, desktop_id)
                return pid
            else:
                counter += 1
            if sleep:
                time.sleep(sleep)
        logger.error("Could not move program (pid=%d) to virtual desktop %s.", pid, desktop_id)
        return None

    def launch_program(self, command, input=None, desktop_id=None, open_async=False, max_tries=3, sleep=None):
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
            max_tries::int
                The # of times moving the program should be tried. If 0,
                it won't be tried to move.
            sleep::float
                The amount of time to sleep before moving the process

        Returns:
            pid::int
                The process id of the created process. May be None
                if the process was not successfully launched.
        """
        return_code, stdout, pid = run_on_command_line(command, input=input, open_async=open_async)
        if return_code is 0 or (return_code is None and open_async):
            logger.info("Launched program (pid=%d) successfully. Trying to move it to desktop %s.", pid, desktop_id)
        else:
            logger.error("Could not run command. Error: %s", stdout)
            return None

        if sleep:
            time.sleep(sleep)

        if max_tries > 0:
            return self.move_program(pid, desktop_id, max_tries, sleep)
        else:
            return pid

    def destroy(self):
        pass

    def save(self, path=None):
        path = path or self.object_persist_path
        save_dict_to_json(self, path)

    def load(self, path=None):
        path = path or self.object_persist_path
        load_dict_from_json(self, path)


CODE_NAME = 'virtual_desktop'
HUMAN_READABLE_NAME = 'VirtualDesktop'
DESKTOP_CLASS = VirtualDesktop if platform.system() is 'Windows' else None
