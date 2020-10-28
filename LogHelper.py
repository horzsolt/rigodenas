import logging

def setup_logger(name, log_file, formatter, level=logging.DEBUG):

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

song_formatter = logging.Formatter('')
song_logger = setup_logger('first_logger', 'songs.log', song_formatter)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = setup_logger('error_logger', 'application.log', formatter)