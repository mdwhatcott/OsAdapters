import os
import shutil
import contextlib


class FileSystem(object):
    def getcwd(self):
        return os.getcwd()

    def chdir(self, location):
        os.chdir(location)

    @contextlib.contextmanager
    def working_location(self, location):
        initial = self.getcwd()
        try:
            self.chdir(location)
            yield
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


class Location(object):
    def __init__(self, path):
        if not os.path.exists(path):
            raise NameError("Path does not exist: {0}".format(path))

        self.path = os.path.abspath(path)

    @property
    def isfile(self):
        return os.path.isfile(self.path)

    @property
    def isdir(self):
        return os.path.isdir(self.path)

    @property
    def filename(self, with_extension=True):
        if not self.isfile:
            return ''

        name = self.components[-1]

        if not with_extension and '.' in name:
            return '.'.join(name.split('.')[:-1])

        return name

    @property
    def extension(self):
        return '' if not self.isfile else self.basename.split('.')[-1]

    @property
    def components(self):
        return self.path.split(os.path.sep)

    @property
    def children(self):
        return [Location(os.path.join(self.path, child)) for child in os.listdir(self.path)]

    @property
    def parent(self):
        if os.path.isfile(self.path):
            return Location(os.path.dirname(self.path))

        return Location(os.path.abspath(os.path.join(self.path, os.path.pardir)))

    def __str__(self):
        return self.path

    def __repr__(self):
        return "Location('{0}')".format(self.path)
