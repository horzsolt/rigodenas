import sys
import os
import pytest

sys.path.append('..')
from local_file_helper import clean_download_directory

@pytest.mark.skip(reason="Not needed atm")
def test_cleaning():
    #clean_download_directory(r'e:\python\Fish_Go_Deep--The_Jazz-(IR237)-WEB-2002-BABAS')

    if not [f for f in os.listdir(r'x:\rigodetools\DOWNLOADS\1122\0-DAY\Deeplow-Chillin_In_The_Sun-(SUPRI083)-WEB-2020-KLIN_INT') if f.endswith('.mp3')]:
        print('FALSE')
    else:
        print('TRUE')