import psycopg2
import os
from loghelper import logger
from configparser import ConfigParser
from datetime import datetime, timezone

class PostgresHelper():

    def __init__(self):

        config_object = ConfigParser()
        config_object.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini"))
        serverinfo = config_object["CONFIG"]

        self.host = serverinfo["POSTGRES_HOST"]
        self.user = serverinfo["POSTGRES_USER"]
        self.pwd = serverinfo["POSTGRES_PWD"]
        self.conn = None

        logger.debug(f"host {self.host}")
        logger.debug(f"user {self.user}")

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, type, value, traceback):
        if (self.conn != None):
            self.conn.close()

    def _disconnect(self):
        if (self.conn != None):
            self.conn.close()

    def _connect(self):
        logger.debug("connect")
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                port=49431,
                database="postgres"
            )
        except Exception as ex:
            logger.error(ex, exc_info=True)
            print(ex)

    def pg_store_record(self, ftpfile):
        
        insert_command = f"INSERT INTO public.rigodetools (time, group1, directory, path, size) VALUES('{datetime.now(timezone.utc)}', '{ftpfile.group}', '{ftpfile.directory}', '{ftpfile.path}', '{ftpfile.size}');"
        try:
            logger.debug(f"pg_store_record {insert_command}")
            cursor = self.conn.cursor()

            cursor.execute(insert_command)

            self.conn.commit()
        except Exception as ex:
            logger.error(ex, exc_info=True)