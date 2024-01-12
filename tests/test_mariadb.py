import sys
import pytest
from src.mariadbhelper import MariaDBHelper

@pytest.mark.skip(reason="no reason of currently testing this")
def test_dailysum():
    with MariaDBHelper() as m:
        m.add_daily_summary("1001", "268 minutes", 146, 12)