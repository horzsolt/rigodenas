import mariadb
import os
from loghelper import logger
from configparser import ConfigParser
import datetime

class MariaDBHelper():

    def __init__(self):

        config_object = ConfigParser()
        config_object.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini"))
        serverinfo = config_object["CONFIG"]

        self.host = serverinfo["MARIADB_HOST"]
        self.user = serverinfo["MARIADB_USER"]
        self.pwd = serverinfo["MARIADB_PWD"]
        self.conn = None
        self.year = str(datetime.datetime.now().year)

        logger.debug(f"host {self.host}")
        logger.debug(f"user {self.user}")

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, type, value, traceback):
        if (self.conn != None):
            self.conn.close()

    def _connect(self):
        logger.debug("connect")
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.pwd,
                host=self.host,
                port=3307,
                database="rigodetools"

            )
        except Exception as ex:
            logger.error(ex, exc_info=True)
            print(ex)

    def add_daily_summary(self, day, execution_time, bt_count, oday_count):

        if (self.conn is None):
            self._connect()

        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO dailysummary (day,executiontime,btcount,odaycount) VALUES (?, ?, ?, ?)", (self.year + day, execution_time, bt_count, oday_count))
            self.conn.commit()
        finally:
            cursor.close()

    def add_daily_detail(self, day, directory_entry, kind):

        if (self.conn is None):
            self._connect()

        cursor = self.conn.cursor()
        try:
            logger.debug(f"INSERT INTO dailydetails (day,directory,kind) VALUES ({self.year + day}, {directory_entry}, {kind})")
            cursor.execute("INSERT INTO dailydetails (day,directory,kind) VALUES (?, ?, ?)", (self.year + day, directory_entry, kind))
            self.conn.commit()
        finally:
            cursor.close()