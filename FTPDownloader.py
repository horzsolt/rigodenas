from LogHelper import logger
from datetime import datetime, timedelta
from FTPHelper import FtpCrawler

#def feedElasticSearch():
    #curl -XPUT http://192.168.0.210:9200/customer?pretty


try:

    today = datetime.now() - timedelta(1)
    today_directory = today.strftime("%m%d")

    logger.debug(today_directory)
    print(today_directory)

    with FtpCrawler() as ftpcrawler:
        ftpcrawler.list_beatport_directory(today_directory)
        ftpcrawler.list_0day_directory(today_directory)

except Exception as ex:
    logger.error(ex, exc_info=True)
    print(ex)
