import sys
import pytest
sys.path.append('..')
from ableton import parse_ableton_project, generate_tracklist

def test_parse():
    list_title, list_time = parse_ableton_project(r'q:\!mix\2020_13\template Project\2020_13.als')
    print(list_title)

    generate_tracklist(r'q:\!mix\2020_13\template Project\2020_13.als')