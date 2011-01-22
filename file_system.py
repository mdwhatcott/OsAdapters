import os
import shutil
import contextlib


class FileSystem(object):
    def getcwd(self):
        return os.getcwd()

    def chdir(self, location):
        os.chdir(location)

    @contextlib.contextmanager
    def working_directory(self, location):
        initial = self.getcwd()
        try:
            self.chdir(location)
            yield
        except Exception:
            raise
        finally:
            self.chdir(initial)

    def isfile(self, path):
        return os.path.isfile(path)

    def isdir(self, location):
        return os.path.isdir(location)

    def open(self, path, mode):
        return open(path, mode)

    def listdir(self, location=None):
        return os.listdir(location) if location else os.listdir(self.getcwd())

    def makedir(self, location):
        os.makedirs(location)

    def remove(self, path, force=False):
        os.remove(path)

    def removetree(self, location, force=False):
        location = os.path.abspath(location)
        if force and location.upper() != 'C:\\':
            for root, dirs, files in os.walk(location, topdown=False):
                for d in dirs:
                    os.remove(os.path.join(root, d))
                for f in files:
                    os.remove(os.path.join(root, f))
        else:
            shutil.rmtree(location)

    def move(self, src, dest):
        shutil.move(src, dest) 

    def copy(self, src, dest):
        shutil.copy(src, dest)
