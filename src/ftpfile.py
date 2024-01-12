class FtpFile:

    def __init__(self, group, directory, path):
        self._group = group
        self._directory = directory
        self._path = path
        self.size = 0

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def group(self):
        return self._group
    
    @group.setter
    def group(self, new_group):
        self._group = new_group    

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
            "size": self.size,
            "path": self._path
        }

    def __str__(self):
        return self._group + " " + str(self.size)