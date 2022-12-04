from loghelper import logger
from datetime import datetime, timedelta
from FTPHelper import FtpCrawler
from codetiming import Timer
import sys

try:

    today = datetime.now() - timedelta(1)
    today_directory = today.strftime("%m%d")

    if (len(sys.argv) == 2):
        today_directory = sys.argv[1]

    logger.debug(today_directory)
    print("Crawling {}".format(today_directory))

    timer = Timer("ftp", text="Finished in {minutes:.1f} minutes")
    with FtpCrawler() as ftpcrawler:

        timer.start()
        ftpcrawler.list_beatport_directory(today_directory)
        ftpcrawler.list_0day_directory(today_directory)
        ftpcrawler.download_queue_bt(today_directory)
        ftpcrawler.download_queue_oday(today_directory)

        timer.stop()
        download_time = Timer.timers["ftp"]

except Exception as ex:
    logger.error(ex, exc_info=True)
    print(ex)
    raise Exception("Report abnormal termination to the NAS scheduler")
