import os
import sys
import string
import contextlib
from subprocess import Popen, PIPE
check_output = None

def replace_check_output(command_args, **kwargs):
    kwargs['stdout'] = PIPE
    return Popen(' '.join(command_args), **kwargs).stdout.read()

try:
    from subprocess import check_output
except ImportError:
    check_output = replace_check_output

_SPACE = string.whitespace[-1]
_BLANK = str()

class Command(object):
    NO_OP = '(...no op...)\n{0}>{1}'

    def __init__(self, text=None):
        self._command = [text] if text is not None else []
        self._working_location = os.getcwd() 
        self._no_op = False
        self._verbose = False
        self._async = False
        self._output = None

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

    def async(self, output=sys.stdout):
        self._async = True
        self._output = output
        return self

    def run(self):
        if self._no_op:
            return self._no_op_report()

        if self._verbose:
            print self._command

        with self._working_context(self._working_location):
            if self._async:
                return Popen(self._command, stdout=self._output, stderr=self._output)

            return check_output(self._command, shell=True)

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
