import sys
from src.ableton import parse_ableton_project, generate_tracklist

def test_parse():
    ableton_file = r'q:\!mix\2023_01\2023_01\2023_01 Project\2023_01.als'
    list_title, list_time = parse_ableton_project(ableton_file)
    print(list_title)

    generate_tracklist(ableton_file)
