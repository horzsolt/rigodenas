from elasticsearch import Elasticsearch
from LogHelper import logger

def es_create_index(index_name="demo"):
    
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
        if not es.indices.exists(index_name):
            es.indices.create(index=index_name, ignore=400, body=settings)
            logger.debug('Index created')
    except Exception as ex:
        logger.error(ex, exc_info=True)

def es_store_record(record, index_name="demo"):
    try:
        es.index(index=index_name, doc_type='songs', body=record)
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
    es_store_record(json)

es_indexname = "rigodetools"
es = Elasticsearch([{'host': '192.168.0.210', 'port': 9200}])
if not es.ping():
    raise Exception("Couldn't connect to ES")
es_create_index()