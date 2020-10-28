from LogHelper import logger
from datetime import datetime, timedelta
from FTPHelper import FtpCrawler

try:

    today = datetime.now() - timedelta(1)
    today_directory = today.strftime("%m%d")

    logger.debug(today_directory)
    print("Start crawling of {}".format(today_directory))

    with FtpCrawler() as ftpcrawler:
        ftpcrawler.list_beatport_directory(today_directory)
        ftpcrawler.list_0day_directory(today_directory)

except Exception as ex:
    logger.error(ex, exc_info=True)
    print(ex)
    raise Exception("Report abnormal termination to the NAS scheduler")
