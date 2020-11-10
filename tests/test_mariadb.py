import sys
import pytest
sys.path.append('..')
from mariadbhelper import MariaDBHelper

@pytest.mark.skip(reason="no reason of currently testing this")
def test_dailysum():
    with MariaDBHelper() as m:
        m.add_daily_summary("1001", "268 minutes", 146, 12)