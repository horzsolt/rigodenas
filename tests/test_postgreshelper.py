import sys
import pytest
from src.ftpfile import FtpFile
from src.postgreshelper import PostgresHelper

def test_insert():
    with PostgresHelper() as p:
        ftpFile = FtpFile("0-DAY", "directory", "path")
        p.pg_store_record(ftpFile)