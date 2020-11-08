from loghelper import logger
from datetime import datetime, timedelta
from ftphelper import FtpCrawler
from codetiming import Timer
import sys

try:

    today = datetime.now() - timedelta(1)
    today_directory = today.strftime("%m%d")

    if (len(sys.argv) == 2):
        today_directory = sys.argv[1]

    logger.debug(today_directory)
    print("Start crawling of {}".format(today_directory))

    with Timer(name="ftp",text="Finished in {minutes:.1f} minutes"):
        with FtpCrawler() as ftpcrawler:
            ftpcrawler.list_beatport_directory(today_directory)
            ftpcrawler.list_0day_directory(today_directory)
            ftpcrawler.download_queue_bt(today_directory)
            ftpcrawler.download_queue_oday(today_directory)
    download_time = Timer.timers["ftp"]

except Exception as ex:
    logger.error(ex, exc_info=True)
    print(ex)
    raise Exception("Report abnormal termination to the NAS scheduler")
