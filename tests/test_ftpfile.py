import sys
import pytest
import src.ftpfile

def test_ftpfile():
    file = ftpfile.FtpFile("BEATPORT__AND__WEBSITE_SECTION", "entry", "path")
    file.size = 123

    print(file.toDict())
