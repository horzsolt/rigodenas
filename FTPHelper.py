import os
from datetime import datetime, timedelta
from dateutil import parser
from loghelper import logger, song_logger
from elastichelper import es_store_record
from string import digits
from songhelper import favourites, banned
from ftpfile import FtpFile
from configparser import ConfigParser
from codetiming import Timer
import difflib
import reconnecting_ftp
from m3u import generate_m3u

class FtpCrawler():

    def __init__(self):

        config_object = ConfigParser()
        config_object.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini"))
        serverinfo = config_object["CONFIG"]

        self.host = serverinfo["HOST"]
        self.user = serverinfo["USER"]
        self.pwd = serverinfo["PWD"]
        self.download_root = serverinfo["DOWNLOAD_ROOT"]

        self.queue_bt = []
        self.queue_oday = []
        self.matcher_list = []

    def __enter__(self):

        #_ftp = ftplib.FTP()
        #_ftp.encoding = 'cp1252'
        #_ftp.set_pasv(True)

        self.ftp = reconnecting_ftp.Client(self.host, 7777, self.user, self.pwd)
        self.ftp.makepasv()
        return self

    def __exit__(self, type, value, traceback):

        logger.debug("Downloaded BT {}".format(len(self.queue_bt)))
        logger.debug("Downloaded 0Day {}".format(len(self.queue_oday)))        
        self.ftp.close()

    def download_queue_bt(self, directory):
        logger.debug("download start: bt")

        self.ftp.cwd("//MP3")
        self.ftp.cwd("BEATPORT__AND__WEBSITE_SECTION")
        self.ftp.cwd(directory)

        if not os.path.exists(self.download_root + directory):
            os.makedirs(self.download_root + directory)

        timer = Timer(text="Track downloaded in {:0.2f} seconds", logger=logger.info)

        for ftpfile in self.queue_bt:
            #print("Current directory {}".format(self.ftp.pwd()))
            #print("cwd to {}".format(ftpfile.directory))

            self.ftp.cwd(ftpfile.directory)

            logger.debug(f"Listing directory {ftpfile.directory}")
            for filename in (path for path in self.ftp.nlst() if path not in ('.', '..')):
                logger.debug(f"Checking filename {filename}")

                destination_dir = os.path.join(self.download_root, directory, ftpfile.group,ftpfile.directory)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                local_filename = os.path.join(destination_dir, filename.replace('-www.groovytunes.org','').replace('_', ' '))

                if not os.path.exists(local_filename):
                    if (ftpfile.size < 52914560):                    
                        logger.info(f"Downloading {filename} to {local_filename}")

                        timer.start()
                        file = open(local_filename, 'wb')
                        self.ftp.retrbinary('RETR '+ filename, file.write)
                        file.close()
                        timer.stop()
                    else:
                        logger.warn(f"Skip oversized file {filename}")
                else:
                    logger.info(f"File already exists {local_filename}.")

            generate_m3u(destination_dir)
            self.ftp.cwd("..")

    def download_queue_oday(self, directory):
        logger.debug("download start: bt")

        self.ftp.cwd("//MP3")
        self.ftp.cwd("0-DAY")
        self.ftp.cwd(directory)

        if not os.path.exists(self.download_root + directory):
            os.makedirs(self.download_root + directory)

        timer = Timer(text="Track downloaded in {:0.2f} seconds", logger=logger.info)

        for ftpfile in self.queue_oday:
            #print("Current directory {}".format(self.ftp.pwd()))
            #print("cwd to {}".format(ftpfile.directory))

            self.ftp.cwd(ftpfile.directory)

            for filename in (path for path in self.ftp.nlst()[1:] if path not in ('.', '..')): #first entry is always a sub directory
                logger.debug(f"Checking filename {filename}")

                destination_dir = os.path.join(self.download_root, directory, ftpfile.group,ftpfile.directory)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                local_filename = os.path.join(destination_dir, filename.replace('-www.groovytunes.org',''))

                if not os.path.exists(local_filename):
                    if (ftpfile.size < 52914560):                    
                        logger.info(f"Downloading {filename} to {local_filename}")

                        timer.start()
                        file = open(local_filename, 'wb')
                        self.ftp.retrbinary('RETR '+ filename, file.write)
                        file.close()
                        timer.stop()
                    else:
                        logger.warn(f"Skip oversized file {filename}")
                else:
                    logger.warn(f"File already exists {local_filename}.")
            self.ftp.cwd("..")            

    def list_beatport_directory(self, directory):
        path = "/MP3/BEATPORT__AND__WEBSITE_SECTION/"        
        self.ftp.cwd(path)
        self.ftp.cwd(directory)
       
        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                logger.debug("Entering directory: {}".format(entry))
                self.ftp.cwd(entry)

                ftpFile = FtpFile("BEATPORT__AND__WEBSITE_SECTION", entry)

                for filename in (path for path in self.ftp.nlst() if path not in ('.', '..')):
                    largest = 0
                    logger.debug("entry {}".format(entry))
                    logger.debug("sub_entry {}".format(filename))
                    logger.debug("path {}".format(path))
                    song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))
                    
                    logger.debug("getting timestamp of {}".format(filename))
                    size = self.ftp.size(filename)

                    if (largest < size):
                        largest = size
                        ftpFile.size = size

                    logger.debug("ftp.size {0}/{1}".format(path + directory, filename))
                    es_store_record(ftpFile.toDict())

                result = [fav_element for fav_element in banned if fav_element.upper() in entry.upper()]
                if (len(result) == 0):
                    result = [fav_element for fav_element in favourites if fav_element.upper() in entry.upper()]
                    if (len(result) > 0):
                        if (len(difflib.get_close_matches(entry, self.matcher_list)) == 0):
                            logger.info(f"Adding to BT q {entry}")
                            self.queue_bt.append(ftpFile)

                self.matcher_list.append(entry)                 
                self.ftp.cwd('..')
            except Exception:
                logger.error("Listing error: ", exc_info=True)

    def list_0day_directory(self, directory):
        path = "/MP3/0-DAY/"
        self.ftp.cwd(path)
        self.ftp.cwd(directory)

        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                logger.debug("Entering directory: " + entry)
                self.ftp.cwd(entry)

                ftpFile = FtpFile("0-DAY", entry)

                for filename in (path for path in self.ftp.nlst()[1:] if path not in ('.', '..')): #first entry is always a sub directory
                    largest = 0
                    logger.debug("entry " + entry)
                    logger.debug("sub_entry " + filename)
                    logger.debug("path " + path)
                    song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))
                    
                    size = self.ftp.size(filename)

                    if (largest < size):
                        largest = size
                        ftpFile.size = size

                    es_store_record(ftpFile.toDict())

                result = [fav_element for fav_element in banned if fav_element.upper() in entry.upper()]
                if (len(result) == 0):
                    result = [fav_element for fav_element in favourites if fav_element.upper() in entry.upper()]
                    if (len(result) > 0):
                        if (len(difflib.get_close_matches(entry, self.matcher_list)) == 0):
                            logger.info(f"Adding to 0-day q {entry}")
                            self.queue_oday.append(ftpFile)

                self.matcher_list.append(entry)
                self.ftp.cwd('..')
            except Exception:
                logger.error("Listing error: ", exc_info=True)