import sys
import pytest
sys.path.append('..')
from ableton import parse_ableton_project, generate_tracklist

def test_parse():
    ableton_file = r'q:\!mix\2021_04\template Project\2021_04.als'
    list_title, list_time = parse_ableton_project(ableton_file)
    print(list_title)

    generate_tracklist(ableton_file)