import os
from ftplib import FTP
from datetime import datetime, timedelta
from dateutil import parser
from loghelper import logger, song_logger
from elastichelper import es_store_record
from string import digits
from songhelper import favourites, banned
from ftpfile import FtpFile
from configparser import ConfigParser

class FtpCrawler():

    def __init__(self):
        self.ftp = FTP()
        self.ftp.encoding = 'cp1252'
        self.ftp.set_pasv(True)
        self.queue = []

    def __enter__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        serverinfo = config_object["SERVERCONFIG"]

        self.ftp.connect(serverinfo["HOST"], 7777)
        self.ftp.login(serverinfo["USER"], serverinfo["PWD"])

        return self

    def __exit__(self, type, value, traceback):
        self.ftp.quit()

    def list_beatport_directory(self, directory):
        path = "/MP3/BEATPORT__AND__WEBSITE_SECTION/"
        self.ftp.cwd(path)
        self.ftp.cwd(directory)
        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                logger.debug("Entering directory: {}".format(entry))
                self.ftp.cwd(entry)
                for filename in (path for path in self.ftp.nlst() if path not in ('.', '..')):
                    logger.debug("entry {}".format(entry))
                    logger.debug("sub_entry {}".format(filename))
                    logger.debug("path {}".format(path))
                    song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))
                    
                    logger.debug("getting timestamp of {}".format(filename))

                    timestamp = self.ftp.voidcmd("MDTM " + filename)[4:].strip()
                    sTime = parser.parse(timestamp).strftime("%Y.%m.%d %H:%M:%S")
                    sDirectory = directory + "/" + entry
                    sFullFilename = path + directory + "/" + entry + "/" + filename
                    sPrettyFilename = filename.replace('-www.groovytunes.org','').lstrip(digits).lstrip('-').replace('_', ' ')
                    size = self.ftp.size(filename)

                    ftpFile = FtpFile("0DAY", sTime, filename, sDirectory, sFullFilename, sPrettyFilename, size)
                    logger.debug("ftp.size {0}/{1}".format(path + directory, filename))
                    es_store_record(ftpFile.toDict())

                    result = [fav_element for fav_element in banned if fav_element.upper() in sDirectory.upper()]
                    if (len(result) == 0):
                        result = [fav_element for fav_element in favourites if fav_element.upper() in sDirectory.upper()]
                        if (len(result) > 0):
                            if (size < 52914560):
                                self.queue.append(ftpFile)


                self.ftp.cwd('..')
            except Exception:
                logger.error("Listing error: ", exc_info=True)

    def list_0day_directory(self, directory):
        path = "/MP3/0-DAY/"
        self.ftp.cwd(path)
        self.ftp.cwd(directory)
        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                logger.debug("Enter directory: " + entry)
                self.ftp.cwd(entry)
                for filename in (path for path in self.ftp.nlst()[1:] if path not in ('.', '..')): #first entry is always a sub directory
                    logger.debug("entry " + entry)
                    logger.debug("sub_entry " + filename)
                    logger.debug("path " + path)
                    song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))
                    
                    logger.debug("getting timestamp of " + filename)
                    timestamp = self.ftp.voidcmd("MDTM " + filename)[4:].strip()
                    sTime = parser.parse(timestamp).strftime("%Y.%m.%d %H:%M:%S")
                    sDirectory = directory + "/" + entry
                    sFullFilename = path + directory + "/" + entry + "/" + filename
                    sPrettyFilename = filename.replace('-www.groovytunes.org','')
                    size = self.ftp.size(filename)
                    extension = os.path.splitext(filename)[1]

                    ftpFile = FtpFile("0DAY", sTime, filename, sDirectory, sFullFilename, sPrettyFilename, size)

                    if (extension == ".mp3"):
                        es_store_record(ftpFile.toDict())
                    else:
                        logger.debug("Extension " + extension + " will not be stored.")
                self.ftp.cwd('..')
            except Exception:
                logger.error("Listing error: ", exc_info=True)