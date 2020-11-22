import sys
import pytest
sys.path.append('..')
from mp3helper import get_audio_info

@pytest.mark.skip(reason="Temporarily disabled")
def test_audio_info():
    get_audio_info(r"q:\!mix\2020_10\10A - 126 - John Summit - Deep End Extended Mix_pn.mp3")
    get_audio_info(r"q:\!mix\2020_10\9A - 123 - Walk The Line Extended Mix_pn.mp3")
    get_audio_info(r"x:\rigodetools\DOWNLOADS\1113\BEATPORT__AND__WEBSITE_SECTION\Robert Babicz - Utopia SYST00222\Robert Babicz - Childhood Original Mix Systematic Recordings.mp3" )