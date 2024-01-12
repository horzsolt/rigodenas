import os
from loghelper import logger, song_logger
from songhelper import favourites, banned, has_valid_year_in_title
from ftpfile import FtpFile
from configparser import ConfigParser
from codetiming import Timer
import difflib
import reconnecting_ftp
from local_file_helper import clean_download_directory
from postgreshelper import PostgresHelper

class FtpCrawler():

    def __init__(self):

        self.pg = PostgresHelper()
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

        self.ftp = reconnecting_ftp.Client(self.host, 7777, self.user, self.pwd, encoding='cp1252')
        self.pg._connect()
        logger.debug("FTP - connecting in active mode...")
        #self.ftp.makepasv()
        return self

    def __exit__(self, type, value, traceback):

        logger.debug("Downloaded BT %s", len(self.queue_bt))
        logger.debug("Downloaded 0Day %s", len(self.queue_oday))
        self.pg._disconnect()
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

            self.ftp.cwd(ftpfile.directory)

            logger.debug("Listing directory %s", ftpfile.directory)
            for filename in (path for path in self.ftp.nlst() if path not in ('.', '..')):
                logger.debug("Checking filename %s ", filename)

                destination_dir = os.path.join(self.download_root, directory, ftpfile.group,
                    ftpfile.directory)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                local_filename = os.path.join(destination_dir,
                    filename.replace('-www.groovytunes.org','').replace('_', ' '))

                if not os.path.exists(local_filename):
                    if ftpfile.size < 52914560:
                        logger.info(f"Downloading {filename} to {local_filename}")

                        timer.start()
                        file = open(local_filename, 'wb')
                        self.ftp.retrbinary('RETR '+ filename, file.write)
                        file.close()
                        timer.stop()

                        self.pg.pg_store_record(FtpFile("DOWNLOAD", ftpfile.directory, ftpfile.path + ftpfile.directory))
                    else:
                        logger.info("Skip oversized file %s" ,filename)
                else:
                    logger.info("File already exists %s", local_filename)

            if (destination_dir):
                clean_download_directory(destination_dir)
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

            #first entry is always a sub directory
            for filename in (path for path in self.ftp.nlst() if path not in ('.', '..')):
                logger.debug("Checking filename %s", filename)
                destination_dir = os.path.join(self.download_root, directory, ftpfile.group,
                    ftpfile.directory)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                local_filename = os.path.join(destination_dir,
                    filename.replace('-www.groovytunes.org',''))

                if filename.startswith('-['):
                    if not os.path.exists(local_filename):
                        os.makedirs(local_filename)
                else:
                    if not os.path.exists(local_filename):
                        if ftpfile.size < 52914560:
                            timer.start()
                            file = open(local_filename, 'wb')
                            self.ftp.retrbinary('RETR '+ filename, file.write)
                            file.close()
                            timer.stop()

                            self.pg.pg_store_record(FtpFile("DOWNLOAD", ftpfile.directory, ftpfile.path + ftpfile.directory))
                        else:
                            logger.info("Skip oversized file %s", filename)
                    else:
                        logger.info("File already exists %s", local_filename)

            clean_download_directory(destination_dir)
            self.ftp.cwd("..")

    def list_beatport_directory(self, directory):
        path = "/MP3/BEATPORT__AND__WEBSITE_SECTION/"
        self.ftp.cwd(path)
        self.ftp.cwd(directory)

        print(path)
        print(directory)

        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                print("Entering directory: {}".format(entry))
                self.ftp.cwd(entry)

                ftpFile = FtpFile("BEATPORT__AND__WEBSITE_SECTION", entry, path + directory)

                largest = 0

                for filename in (path for path in self.ftp.nlst() if path not in ('.', '..')):
                    logger.debug("entry {}".format(entry))
                    logger.debug("sub_entry {}".format(filename))
                    logger.debug("path {}".format(path))
                    song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))

                    logger.debug("getting timestamp of {}".format(filename))
                    size = self.ftp.size(filename)

                    if (largest < size):
                        largest = size
                    ftpFile.size = size

                logger.debug(ftpFile)
                self.pg.pg_store_record(ftpFile)


                result = [fav_element for fav_element in banned if fav_element.upper() in entry.upper().replace(' ', '_')]
                if (len(result) == 0):
                    if has_valid_year_in_title(entry):
                        result = [fav_element for fav_element in favourites if fav_element.upper() in entry.upper().replace(' ', '_')]
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

                ftpFile = FtpFile("0-DAY", entry, path + directory)

                largest = 0

                for filename in (path for path in self.ftp.nlst()[1:] if path not in ('.', '..')): #first entry is always a sub directory
                    logger.debug("entry " + entry)
                    logger.debug("sub_entry " + filename)
                    logger.debug("path " + path)
                    song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))

                    size = self.ftp.size(filename)

                    if (largest < size):
                        largest = size
                        ftpFile.size = size

                self.pg.pg_store_record(ftpFile)

                result = [fav_element for fav_element in banned if fav_element.upper() in entry.upper().replace(' ', '_')]
                if (len(result) == 0):
                    if has_valid_year_in_title(entry):
                        result = [fav_element for fav_element in favourites if fav_element.upper() in entry.upper().replace(' ', '_')]
                        if (len(result) > 0):
                            if (len(difflib.get_close_matches(entry, self.matcher_list)) == 0):
                                logger.info(f"Adding to 0-day q {entry}")
                                self.queue_oday.append(ftpFile)

                self.matcher_list.append(entry)
                self.ftp.cwd('..')
            except Exception:
                logger.error("Listing error: ", exc_info=True)
