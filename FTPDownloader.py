import os
import logging
from ftplib import FTP
from datetime import datetime, timedelta
from dateutil import parser
from elasticsearch import Elasticsearch

def setup_logger(name, log_file, formatter, level=logging.DEBUG):

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

#def feedElasticSearch():
    #curl -XPUT http://192.168.0.210:9200/customer?pretty

def es_create_index(es_object, index_name="demo"):
    
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "members": {
                "dynamic": "strict",
                "properties": {
                    "group": {
                        "type": "text"
                    },
                    "date": {
                        "type": "date",
                        "format": "yyyy.MM.dd HH:mm:ss"
                    },
                    "directory": {
                        "type": "text"
                    },                    
                    "filename": {
                        "type": "text"
                    },
                    "full_filename": {
                        "type": "text"
                    },
                    "pretty_filename": {
                        "type": "text"
                    }                    
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            logger.debug('Index created')
    except Exception as ex:
        logger.error(ex, exc_info=True)

def es_store_record(es_object, record, index_name="demo"):

    try:
        es_object.index(index=index_name, doc_type='songs', body=record)
    except Exception as ex:
        logger.error(ex, exc_info=True)

def create_json(group, time, filename, directory, full_filename, pretty_filename, size):
    logger.debug("About to create JSON")

    json = {
        "group": group,
        "date": time,
        "filename": filename,
        "directory": directory,        
        "full_filename": full_filename,
        "pretty_filename": pretty_filename
    }

    logger.debug(json)
    es_store_record(es, json)


def list_beatport_directory(directory):
    
    path = "/MP3/BEATPORT__AND__WEBSITE_SECTION/"
    ftp.cwd(path)
    ftp.cwd(today_directory)
    for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
        try:
            logger.debug("Enter directory: " + entry)
            ftp.cwd(entry)
            for filename in (path for path in ftp.nlst() if path not in ('.', '..')):
                logger.debug("entry " + entry)
                logger.debug("sub_entry " + filename)
                logger.debug("path " + path)
                song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))
                
                logger.debug("getting timestamp of " + filename)
                timestamp = ftp.voidcmd("MDTM " + filename)[4:].strip()
                sTime = parser.parse(timestamp).strftime("%Y.%m.%d %H:%M:%S")
                sDirectory = directory + "/" + entry
                sFullFilename = path + directory + "/" + entry + "/" + filename
                sPrettyFilename = filename.replace('-www.groovytunes.org','')
                sSize = ftp.size(filename)

                logger.debug('ftp.size ' + path + directory + "/" + filename)
                create_json("BEATPORT", sTime, filename, sDirectory, sFullFilename, sPrettyFilename, sSize)
            ftp.cwd('..')
        except Exception:
            logger.error("Listing error: ", exc_info=True)

def list_0day_directory(directory):
    
    path = "/MP3/0-DAY/"
    ftp.cwd(path)
    ftp.cwd(today_directory)
    for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
        try:
            logger.debug("Enter directory: " + entry)
            ftp.cwd(entry)
            for filename in (path for path in ftp.nlst()[1:] if path not in ('.', '..')): #first entry is always a sub directory
                logger.debug("entry " + entry)
                logger.debug("sub_entry " + filename)
                logger.debug("path " + path)
                song_logger.info(directory + "," + filename.replace('-www.groovytunes.org',''))
                
                logger.debug("getting timestamp of " + filename)
                timestamp = ftp.voidcmd("MDTM " + filename)[4:].strip()
                sTime = parser.parse(timestamp).strftime("%Y.%m.%d %H:%M:%S")
                sDirectory = directory + "/" + entry
                sFullFilename = path + directory + "/" + entry + "/" + filename
                sPrettyFilename = filename.replace('-www.groovytunes.org','')
                sSize = ftp.size(filename)
                extension = os.path.splitext(filename)[1]

                if (extension == ".mp3"):
                    create_json("BEATPORT", sTime, filename, sDirectory, sFullFilename, sPrettyFilename, sSize)
                else:
                    logger.debug("Extension " + extension + " will not be stored.")
            ftp.cwd('..')
        except Exception:
            logger.error("Listing error: ", exc_info=True)            

es_indexname = "customer"
song_formatter = logging.Formatter('')
song_logger = setup_logger('first_logger', 'songs.log', song_formatter)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = setup_logger('error_logger', 'application.log', formatter)


try:

    es = Elasticsearch([{'host': '192.168.0.210', 'port': 9200}])
    if not es.ping():
        raise Exception("Couldn't connect to ES")

    ftp = FTP()
    ftp.encoding = 'cp1252'
    ftp.set_pasv(True)

    ftp.connect(os.environ.get('FTP'), 7777)
    ftp.login(os.environ.get('FTP_USER'), os.environ.get('FTP_PWD'))

    today = datetime.now() - timedelta(1)
    today_directory = today.strftime("%m%d")

    logger.debug(today_directory)
    print(today_directory)

    es_create_index(es)

    list_beatport_directory(today_directory)
    list_0day_directory(today_directory)

    ftp.quit()

except Exception as ex:
    logger.error(ex, exc_info=True)
    print(ex)
