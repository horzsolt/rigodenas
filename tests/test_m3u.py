import sys
import pytest
from src.m3u import generate_m3u

@pytest.mark.skip(reason="Temporarily disabled")
def test_m3u_gen():
    generate_m3u(r"x:\rigodetools\DOWNLOADS\1102\BEATPORT__AND__WEBSITE_SECTION\Beatport Top 10 Downloads 2020-11-01")