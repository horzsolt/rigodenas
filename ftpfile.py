class FtpFile:

    def __init__(self, group, time, filename, directory, full_filename, pretty_filename, filesize):
        self.__group = group
        self.__time = time
        self.__filename = filename
        self.__directory = directory
        self.__full_filename = full_filename
        self.__pretty_filename = pretty_filename
        self.__filesize = filesize

    @property
    def time(self):
        return self.__time

    @property
    def filename(self):
        return self.__filename

    @property
    def directory(self):
        return self.__directory

    @property
    def full_filename(self):
        return self.__full_filename

    @property
    def pretty_filename(self):
        return self.__pretty_filename

    @property
    def filesize(self):
        return self.__filesize
    
    def toDict(self):
        return {
            "group": self.__group,
            "date": self.__time,
            "filename": self.__filename,
            "directory": self.__directory,        
            "full_filename": self.__full_filename,
            "pretty_filename": self.__pretty_filename,
            "size": self.__filesize
        }
