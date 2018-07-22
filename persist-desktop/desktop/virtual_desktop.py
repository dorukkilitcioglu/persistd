from io import BytesIO
import json
import logging
import os
import requests
from shutil import rmtree
from zipfile import ZipFile

from util.command_line import run_on_command_line

from desktop.base_desktop import BaseDesktop

logger = logging.getLogger(__name__)


class VirtualDesktop(BaseDesktop):

    # ID of the currently used virtual desktop
    # Note that this may change if another desktop is
    # closed
    virtual_desktop_id = None

    # Path to VirtualDesktop.exe
    exe_path = None

    def __init__(self, base_path, path):
        super().__init__(base_path, path)

        possible_exe_path = os.path.join(path, 'VirtualDesktop.exe')
        if os.path.exists(possible_exe_path):
            self.exe_path = possible_exe_path
        if not self.exe_path:
            self._setup()

    def _setup(self):
        logger.info("Downloading VirtualDesktop from Github...")
        package_url = 'https://github.com/MScholtes/VirtualDesktop/archive/11597438e9559cbe19ef2927451129adfe6a6704.zip'
        zip_raw = requests.get(package_url)

        zip_path = os.path.join(self.path, 'VirtualDesktop')
        logger.info("Extracting VirtualDesktop contents to %s", zip_path)
        zip_bytes = BytesIO(zip_raw.content)
        zip_file = ZipFile(zip_bytes)
        zip_file.extractall(zip_path)

        logger.info("Installing VirtualDesktop...")
        install_dir = os.path.join(zip_path, 'VirtualDesktop-11597438e9559cbe19ef2927451129adfe6a6704')
        cwd = os.getcwd()
        os.chdir(install_dir)
        return_code, stdout, _ = run_on_command_line(["Compile.bat"], input='.'.encode('utf-8'))
        os.chdir(cwd)
        if return_code is 0:
            logger.info("Successfully installed VirtualDesktop!")
        else:
            # TODO error
            logger.error("Could not install VirtualDesktop! Error: %s", str(stdout))

        logger.info("Cleaning up VirtualDesktop installation files...")
        exe_path = os.path.join(self.path, 'VirtualDesktop.exe')
        os.rename(os.path.join(install_dir, 'VirtualDesktop.exe'), exe_path)
        rmtree(zip_path)
        self.exe_path = exe_path

        logger.info("VirtualDesktop is ready to go!")

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

    def launch_program(self, command, input=None, desktop_id=None):
        """ Launches a program, with optional args, at a given desktop.
        If desktop_id is None, should launch at the created desktop.
        """

        return_code, stdout, pid = run_on_command_line(command, input=input)
        if return_code is not 0:
            logger.error("Could not run command. Error: %s", stdout)
            return False
        else:
            logger.info("Launched program (pid=%d) successfully. Trying to move it to desktop %s.", pid, desktop_id)

        desktop_id = desktop_id if desktop_id is not None else self.virtual_desktop_id
        return_code, stdout, _ = run_on_command_line([self.exe_path, '-GetDesktop:%s' % desktop_id, '-MoveWindow:%d' % pid])
        if return_code is 0:
            logger.info("Moved program (pid=%d) to virtual desktop %s successfully.", pid, desktop_id)
            return True
        else:
            logger.error("Could not move program (pid=%d) to virtual desktop %s.", pid, desktop_id)
            return False

        # Instead just switch to the given desktop and pray to god it works
        """
        if self.switch_to_desktop(desktop_id=desktop_id):
            return_code, stdout, pid = run_on_command_line(command, input=input)
            if return_code is not 0:
                logger.error("Could not run command. Error: %s", stdout)
                return False
            else:
                logger.info("Launched program (pid=%d) successfully.", pid)
                return True
        else:
            return False
        """
    def save(self, path=None):
        path = path or self.filename_vd
        with open(path, 'w') as fp:
            json.dump(self.__dict__, fp)

    def load(self, path=None):
        path = path or self.filename_vd
        with open(path, 'r') as fp:
            self.__dict__.update(json.load(fp))

    @property
    def os(self):
        return ('Windows', '10')

    @property
    def filename_vd(self, path=None):
        path = path or self.path
        return os.path.join(self.path, 'vd.json')
