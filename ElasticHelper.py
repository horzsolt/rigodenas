from elasticsearch import Elasticsearch
from LogHelper import logger
from configparser import ConfigParser

def es_create_index():
    
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
        if not es.indices.exists(es_index_name):
            es.indices.create(index=es_index_name, ignore=400, body=settings)
            logger.debug('Index created')
    except Exception as ex:
        logger.error(ex, exc_info=True)

def es_store_record(record):
    try:
        es.index(index=es_index_name, doc_type='songs', body=record)
    except Exception as ex:
        logger.error(ex, exc_info=True)

config_object = ConfigParser()
config_object.read("config.ini")
elasticinfo = config_object["ELASTICCONFIG"]

es_index_name = elasticinfo["INDEX"]
es = Elasticsearch([{'host': '192.168.0.210', 'port': 9200}])
if not es.ping():
    raise Exception("Couldn't connect to ES")
es_create_index()