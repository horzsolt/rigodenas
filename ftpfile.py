class FtpFile:

    def __init__(self, group, directory, size=0):
        self.__group = group
        self.__directory = directory

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def group(self):
        return self.__group

    @property
    def directory(self):
        return self.__directory

    def toDict(self):
        return {
            "group": self.__group,
            "directory": self.__directory,  
            "size": self.__size      
        }
