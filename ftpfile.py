class FtpFile:

    def __init__(self, group, directory, path, size=0):
        self._group = group
        self._directory = directory
        self._path = path

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def group(self):
        return self._group

    @property
    def directory(self):
        return self._directory

    @property
    def path(self):
        return self._path

    def toDict(self):
        return {
            "group": self._group,
            "directory": self._directory,
            "size": self._size,
            "path": self._path
        }
