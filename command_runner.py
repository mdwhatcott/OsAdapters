import subprocess
from libs import file_system
from file_system import FileSystem


class CommandRunner(object):
    def __init__(self, file_system=None, verbose_mode=False):
        self.file_system = file_system or FileSystem(verbose_mode=verbose_mode)
        self.verbose_mode = verbose_mode

    def run(self, command, working_location='.'):
        with self.file_system.working_location(working_location):
            return _run_command(command)

    def _run_command(self, command):
        self._print(command)
        output = subprocess.check_output(command.split(), shell=True)
        self._print(output)

        return output

    def run_async(self, command, working_location='.'):
        with self.file_system.working_location(working_location):
            return _return_code_from(command)

    def _return_code_from(self, command):
        self._print(command)
        return subprocess.call(command.split(), shell=True)

    def _print(self, stuff):
        if self.verbose_mode:
            print stuff
