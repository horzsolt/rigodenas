import difflib

def test_list_diff():
    lst = ["Arapu - Anthology EP MTRZ 011","Asael Weiss - 32.8905 N 35.5116 E PRISMA2", "Chrissy - THE COOL RANCH COLLECTION Cool Ranch", "Chrissy - THE COOL RANCH COLLECTION RANCH006"]
    assert len(difflib.get_close_matches("Chrissy - THE COOL RANCH COLLECTION RANCH006", lst)) > 1

def test_list_diff_2():
    lst = ["Slam-Strange_Dayz__Volume_One-SINGLE-WEB-2020-WAV", "Slam-Strange_Dayz__Volume_Two-SINGLE-WEB-2020-WAV"]
    assert len(difflib.get_close_matches("Slam-Strange_Dayz", lst)) == 0

def test_list_diff_3():
    lst = ["Slam-Strange_Dayz__Volume_One-SINGLE-WEB-2020-WAV"]
    assert len(difflib.get_close_matches("Slam-Strange_Dayz__Volume_Two-SINGLE-WEB-2020-WAV", lst)) == 1

def test_list_diff_4():
    lst = ["Slam-Strange_Dayz__Volume_Two-SINGLE-WEB-2020-WAV"]
    assert len(difflib.get_close_matches("Slam-Strange_Dayz__Volume_One-SINGLE-WEB-2020-WAV", lst, cutoff=1.0)) == 0

def test_list_diff_5():
    lst = ["Slam-Strange_Dayz__Volume_Two-SINGLE-WEB-2020-WAV"]
    assert len(difflib.get_close_matches("Slam-Strange_Dayz__Volume_Two-SINGLE-WEB-2020-WAV", lst, cutoff=1.0)) == 1

def test_list_diff_6():
    lst = ["Browncoat-Edge_Of_Time-(SYYK119)-WEB-2020-AFO", "Browncoat--Edge_Of_Time-(SYYK119)-WEB-2020-BABAS"]
    assert len(difflib.get_close_matches("Browncoat--Edge_Of_Time-(SYYK119)-WEB-2020-BABAS", lst)) == 2
