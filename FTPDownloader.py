from ftplib import FTP
import logging
from datetime import date
import os

def setup_logger(name, log_file, formatter, level=logging.DEBUG):

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def list_beatport_directory(directory):
    for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
        try:
            ftp.cwd(entry)
            for sub_entry in (path for path in ftp.nlst() if path not in ('.', '..')):
                song_logger.info(directory + "," + sub_entry.replace('-www.groovytunes.org',''))
            ftp.cwd('..')
        except Exception:
            logger.error("Listing error: ", exc_info=True)

#def feedElasticSearch():
    #curl -XPUT http://192.168.0.210:9200/customer?pretty


song_formatter = logging.Formatter('')
song_logger = setup_logger('first_logger', 'songs.log', song_formatter)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = setup_logger('error_logger', 'application.log', formatter)


try:
    ftp = FTP()
    ftp.set_pasv(True)

    ftp.connect(os.environ.get('FTP'), 7777)
    ftp.login(os.environ.get('FTP_USER'), os.environ.get('FTP_PWD'))

    today = date.today()
    today_directory = today.strftime("%m%d")

    logger.debug(today_directory)

    #BEATPORT__AND__WEBSITE_SECTION
    ftp.cwd("MP3")
    ftp.cwd("BEATPORT__AND__WEBSITE_SECTION")
    ftp.cwd(today_directory)
    list_beatport_directory(today_directory)

    ftp.quit()

except Exception:
    logger.error("Fatal error in main loop", exc_info=True)
