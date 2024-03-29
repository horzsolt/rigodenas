import re
import datetime

favourites = ("TALE_OF_US", "UMEK", "ANJUNA", "JEROME_ISMA", "BUUREN", "DIGWEED","SAIZ",
            "PETE_TONG", "PETE.TONG", "DOORN", "GUY_J", "GUY.J", "NICK_WARREN",
            "NICK.WARREN", "SASHA", "MACEO_PLEX",
            "ADVISOR", "NEWIK", "MUSIC_KILLERS", "MINILOGUE", "PIG_DAN", "WATERMAT", "SHOWTEK",
            "MANTEY","TODD_TERJE", "MATTZO",
            "WESTBAM", "BERGHEAU", "BOOKA_SHADE", "BLIZZARD", "RANK1", "RANK_1", "KOLETZKI",
            "KALKBRENNER", "REX_MUNDI", "DASH_BERLIN", "ORJAN_NIELSEN",
            "GARETH_EMERY", "BLOMQVIST", "NADJALIND", "NADJA_LIND", "EXTRAWELT", "SCAVO",
            "KOLLEKTIV", "BERLIN", "DAHLBACK", "BENASSI", "VARIOUS",
            "COMPILED", "COMPILATION", "GUETTA", "HARRIS", "DUMONT", "CLAPTONE", "ZEDD_",
            "MARK_KNIGHT", "SHEPARD", "FEDDE_LE_GRAND", "ROGER_SHAH", "KYAU",
            "ABOVE",
            "BEST", "SELECTED", "SELECTION", "EXCLUSIVE", "_HEIDI", "HAWTIN", "GARRIX",
            "BEN_KLOCK", "TROXLER", "EATS_EVERYTHING", "COLLECTION",
            "HOT_SINCE", "MARCO_CAROLA", "KLARTRAUM", "MAYA_JANE_COL", "SVEN_VATH", "JACK_MASTER",
            "LUMEN", "NINA_KRAVIZ", "GARNIER", "LIEBING",
            "DAMIAN_LAZARUS", "CARL_COX", "LEE_BURRIDGE", "JORIS_VOORN", "BUTCH", "ZABIELA",
            "CATZ", "CATTANEO", "JEFF_MILLS",
            "JUSTIN_MARTIN", "LAWLER", "PACO_OSUNA", "TANZMANN", "DEETRON", "BENN_FINN",
            "TIMO_MAAS", "PICKS", "FABRIC",
            "GLOBAL_UNDERGROUND", "MOBY", "SERIES", "HOXTON", "ESSENTIAL", "MOONBEAM", "RA-TOP",
            "RA_TOP", "TRACKS", "BUDAI",
            "HUNGARY", "BUDAPEST", "_SOUNDS", "PODCAST", "MANTZUR", "VANNELLI", "HAWTIN",
            "TRENTEM", "CHYMERA", "SCUBA", "GUY_GERBER", "ZUSAMMENKLANG",
            "EULBERG, HAZENDONK", "RILEY_REINHOLD", "_TOP", "CD_POOL", "TRANCE", "RESIDENT",
            "ADVISOR", "FABRIK", "WILLCOX", "TYDI", "ANTHOLOGY",
            "ADRIATIQUE", "MARLO", "BUDAKID", "YOTTO", "BICEP", "GHEIST", "THRILLSEEKERS",
            "KLARTRAUM", "DOSEM", "BUDAKID", "EULBERG", "BABIC", "AUDIOJACK",
            "CHART", "_RA_", "TECHNO", "BREJCHA", "TENSAL", "BEATPORT", "KASSAR", "TAPIA",
            "ROMBOY", "BODZIN", "KOLLAR", "TUBE",
            "WASSERMANN", "TENAGLIA", "BOHMER", "KOLSCH", "Moudaber", "Camelphat", "Troxler",
            "Ellen_Allien", "Artbat", "VOORN", "_BIBI", "Disclosure",
            "Dubfire", "FERRER", "Liebing", "Gorgon", "Loco_Dice", "Adriatique", "Monika_Kruse",
            "Zabiela", "Fancuilli", "Witte", "Adam_Beyer", "Amelie_Lens",
            "Peggy_Gou", "En_Pure", "De_Luca", "ANNA", "Carola", "Solardo", "Solomun", "Hawtin",
            "Maya_Jane_Coles", "Nastia", "Rebekah", "VonStroke", "La_Fleur",
            "space_92", "monkey_safari", "Schories", "Bushwacka", "weska", "eelke", "gutenn",
            "pugliesi", "BLR_", "Oxia", "Masseyeff", "JAAR",
            "SHANE54", "SHANE_54", "Tenerfuse", "Abity", "Anakim", "ANUQRAM", "COCHO", "Neuland",
            "Einmusik", "evgeny_lebedev", "FLOA", "humantronic", "capuano",
            "Léger", "LEGER", "MUIR", "Kolsch", "Monolink", "Moonbootica", "Federico_Geckard", 
            "Lilly_Palmer", "Lilly.Palmer", "rodhad", "ignez", "lacchesi", "mekkanikka")

banned = ("AFRO", "HARDSTYLE", "HARD", "GOA", "DRUM_AND_BASS", "_PSY_", "90S", "TRAP_", "TANZ",
        "CHILLHOUSE", "RETRO","HOT_DANCE", "EDM", "TECH.HOUSE",
          "TECH HOUSE", "TECH_HOUSE", "DANCE", "BASS", "TRAXSOURCE")

def has_valid_year_in_title(title):
    year = re.search("(\\d{4})", title)
    if (year):
        if (year.group() == datetime.datetime.now().strftime("%Y")):
            return True
    return False
