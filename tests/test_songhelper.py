import pytest
import logging
import difflib
from src.songhelper import banned,favourites,has_valid_year_in_title

LOGGER = logging.getLogger(__name__)

@pytest.mark.parametrize("directoryName", 
    ("Ron_Ractive-Mod_Tech_300-(10266762)-WEB-2023-SUNBEAM", 
    "Steve_Sibra-Atlantite_EP-(NATBLACK402)-WEB-2022-AFO", 
    "Rebel_Garden-Spirits_Unbound-(TIB002)-WEB-2023-SUNBEAM",
    "Johannes Albert - Strahlemann Alan Dixon Remix FMSTRAHLEMANNC",
    "Traxsource Hype Chart January 2nd 2023",
    "Luciano Candia - Low EP HBT429",
    "Prisma Deer - Caribbean Sky SNDRSDGTL119",
    "VA-Tracks_With_No_Name-(SIXLP_001)-2LP-1993-KINDA"))

def test_is_not_fav_or_banned(directoryName):
    matcher_list = []
    matched = 0
    result = [fav_element for fav_element in banned if fav_element.upper() in directoryName.upper().replace(' ', '_')]

    if (len(result) == 0):
        LOGGER.info("%s is NOT banned.", directoryName)

        if not has_valid_year_in_title(directoryName):
            LOGGER.info("Year is not the current one")
        else:
            result = [fav_element for fav_element in favourites if fav_element.upper() in directoryName.upper().replace(' ', '_')]
            if (len(result) > 0):
                LOGGER.info(result)
                if (len(difflib.get_close_matches(directoryName, matcher_list)) == 0):
                    matched = matched + 1
                    LOGGER.info("Adding to BT q %s ", directoryName)
    else:
        LOGGER.info("%s IS banned.", directoryName)
    
    assert matched == 0

