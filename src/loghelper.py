import logging
import sys

def setup_logger(name, log_file, formatter, level=logging.DEBUG):

    handler = logging.FileHandler(log_file, encoding = "UTF-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

song_formatter = logging.Formatter('')
song_logger = setup_logger('first_logger', 'songs.log', song_formatter)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
##logger = setup_logger('error_logger', 'application.log', formatter, logging.DEBUG)
logging.basicConfig(filename="application.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)