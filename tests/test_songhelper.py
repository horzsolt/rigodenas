import sys
import pytest
import logging
import difflib
sys.path.append('..')
from songhelper import banned,favourites

LOGGER = logging.getLogger(__name__)

@pytest.mark.parametrize("directoryName", 
    ("Ron_Ractive-Mod_Tech_300-(10266762)-WEB-2023-SUNBEAM", 
    "Steve_Sibra-Atlantite_EP-(NATBLACK402)-WEB-2022-AFO", 
    "Rebel_Garden-Spirits_Unbound-(TIB002)-WEB-2023-SUNBEAM"))

def test_banned(directoryName):
    matcher_list = []
    result = [fav_element for fav_element in banned if fav_element.upper() in directoryName.upper().replace(' ', '_')]
    if (len(result) == 0):
        LOGGER.info(f"{directoryName} is NOT banned.")

        result = [fav_element for fav_element in favourites if fav_element.upper() in directoryName.upper().replace(' ', '_')]
        if (len(result) > 0):
            LOGGER.info(result)
            if (len(difflib.get_close_matches(directoryName, matcher_list)) == 0):
                LOGGER.info(f"Adding to BT q {directoryName}")        
    else:
        LOGGER.info(f"{directoryName} IS banned.")

