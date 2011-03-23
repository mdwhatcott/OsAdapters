import os
import string
import contextlib
import subprocess

_SPACE = string.whitespace[-1]
_BLANK = str()

class Command(object):
    NO_OP = '(...no op...)\n{0}>{1}'
    STDOUT_ARG = 'stdout'

    def __init__(self, text=None):
        self._command = [text] if text is not None else []
        self._working_location = os.getcwd() 
        self._no_op = False
        self._verbose = False
        self._blank_out = BlankOut()

    def no_op(self): 
        self._no_op = True
        return self

    def verbose(self): 
        self._verbose = True
        return self

    def arg(self, argument):
        self._command.append(argument)
        return self
        
    def args(self, arguments): 
        self._command.extend(arguments)
        return self

    def within(self, working_location): 
        self._working_location = working_location
        return self

    def run(self):
        if self._no_op:
            return self._no_op_report()

        if self._verbose:
            print self._command

        with self._working_context(self._working_location):
            return subprocess.check_output(self._command, shell=True)

    def run_async(self, *popenargs, **kwargs):
        if self._no_op:
            return self._no_op_report()

        if self._verbose:
            print self._command

        if Command.STDOUT_ARG not in kwargs:
            kwargs[Command.STDOUT_ARG] = self._blank_out

        with self._working_context(self._working_location):
            return subprocess.Popen(self._command, *popenargs, **kwargs)

    def _no_op_report(self):
        print Command.NO_OP.format(self._working_location, _SPACE.join(self._command))
        return _BLANK

    @contextlib.contextmanager
    def _working_context(self, location):
        initial = os.getcwd()
        try:
            os.chdir(location)
            yield
        finally:
            os.chdir(initial)


class BlankOut(object):
    def write(self, output): pass
    def fileno(self): return int()
