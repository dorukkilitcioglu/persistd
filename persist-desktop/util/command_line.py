import os
import subprocess

from util import const


def run_on_command_line(command, input=None):
    """ Runs a command on command line

    Args:
        command::[str]
            The command to run. The first element in list is the
                executable, the rest are the arguments
        input::bytes
            The input to be fed in as STDIN

    Returns:
        return_code::int
            The return code of the executed command
        stdout::str
            The output of the command as a string, or an error object
            if the command was not executed successfully
        pid::int
            The process id of the created process
    """
    sub = subprocess.Popen(command, stdin=subprocess.PIPE if input else None, stdout=subprocess.PIPE)
    stdout, stderr = sub.communicate(input=input)
    sub.poll()
    try:
        return sub.returncode, stdout.decode('utf-8'), sub.pid
    except (AttributeError, UnicodeDecodeError) as err:
        return sub.returncode, err, -1


def kill_mutant(process_name, object_name):
    """ Kills a process mutant to make sure everything opens
    up at the right window.
    """

    # First, set up the environmental variables that the script needs
    os.environ[const.ENV_MUTANT_PROCESS_NAME] = process_name
    os.environ[const.ENV_MUTANT_OBJECT_NAME] = object_name

    # Then, run the actual batch script
    util_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(util_dir, 'windows', 'kill_mutant.bat')
    return_code, _, _ = run_on_command_line([file_path])

    # Even if there was an error, we first unset the environmental variables
    os.environ[const.ENV_MUTANT_PROCESS_NAME] = ""
    os.environ[const.ENV_MUTANT_OBJECT_NAME] = ""

    # Return true if there wasn't any errors
    return return_code == 0
