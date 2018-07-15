import subprocess


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
