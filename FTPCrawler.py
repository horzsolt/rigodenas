from loghelper import logger
from datetime import datetime, timedelta
from ftphelper import FtpCrawler
from codetiming import Timer
from mariadbhelper import MariaDBHelper
import sys

try:

    today = datetime.now() - timedelta(1)
    today_directory = today.strftime("%m%d")

    if (len(sys.argv) == 2):
        today_directory = sys.argv[1]

    logger.debug(today_directory)
    print("Start crawling of {}".format(today_directory))

    timer = Timer("ftp", text="Finished in {minutes:.1f} minutes")
    with FtpCrawler() as ftpcrawler:

        timer.start()
        ftpcrawler.list_beatport_directory(today_directory)
        #ftpcrawler.list_0day_directory(today_directory)
        #ftpcrawler.download_queue_bt(today_directory)
        #ftpcrawler.download_queue_oday(today_directory)

        timer.stop()
        download_time = Timer.timers["ftp"]

        with MariaDBHelper() as mariadb:
            mariadb.add_daily_summary(today_directory, f"Finished in {download_time:1f} minutes", len(ftpcrawler.queue_bt), len(ftpcrawler.queue_oday))

            for ftpfile in ftpcrawler.queue_bt:
                mariadb.add_daily_detail(today_directory, ftpfile.directory, "BEATPORT")

            for ftpfile in ftpcrawler.queue_oday:
                mariadb.add_daily_detail(today_directory, ftpfile.directory, "0-DAY")

except Exception as ex:
    logger.error(ex, exc_info=True)
    print(ex)
    raise Exception("Report abnormal termination to the NAS scheduler")
