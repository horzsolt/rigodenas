import gzip
import tempfile
import shutil
import os
import xmltodict
import datetime

def __convert_millisec_to_time__(str_time):
    time = int(str_time) % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time

    #print(str(datetime.timedelta(seconds = int(str_time))))
    return "%d:%d:%d" % (hour, minutes, seconds)

def __clean_audio_title__(title):
    new_title = title
    if (title.endswith("_pn")):
        new_title = title[0:-3]
    splitted = new_title.split('-')
    if (len(splitted) > 2):
        new_title = ""
        for i in range(2, len(splitted)):
            new_title += splitted[i]
    return new_title.strip()

def generate_tracklist(ableton_project_file):
    dir_path = os.path.dirname(os.path.realpath(ableton_project_file))
    filename = os.path.splitext(ableton_project_file)[0] + ".txt"
    fullpath = os.path.join(dir_path, filename)

    print(fullpath)

    tracklist, timelist = parse_ableton_project(ableton_project_file)

    if (os.path.exists(fullpath)):
        os.remove(fullpath)

    with open(fullpath, "w") as file:
        for idx, tracktitle in enumerate(tracklist):
            file.write(str(idx + 1) + ". " + tracktitle + "\n")

def generate_cue_sheet():
    #https://en.wikipedia.org/wiki/Cue_sheet_(computing)
    pass

def parse_ableton_project(ableton_project_file):
    with open(gunzip_shutil(ableton_project_file)) as fd:
        doc = xmltodict.parse(fd.read())
        first_audio_track = (doc['Ableton']['LiveSet']['Tracks']['AudioTrack'])[0]['DeviceChain']['MainSequencer']['Sample']['ArrangerAutomation']['Events']['AudioClip']
        second_audio_track = (doc['Ableton']['LiveSet']['Tracks']['AudioTrack'])[1]['DeviceChain']['MainSequencer']['Sample']['ArrangerAutomation']['Events']['AudioClip']

        track_list_first_title = list([__clean_audio_title__(audioclip['Name']['@Value']) for audioclip in first_audio_track])
        track_list_second_title = list([__clean_audio_title__(audioclip['Name']['@Value']) for audioclip in second_audio_track])

        track_list_first_time = list([__convert_millisec_to_time__(audioclip['@Time']) for audioclip in first_audio_track])
        track_list_second_time = list([__convert_millisec_to_time__(audioclip['@Time']) for audioclip in second_audio_track])

        flatlist_title = []
        for item in list(zip(track_list_first_title, track_list_second_title)):
            flatlist_title.append(item[0])
            flatlist_title.append(item[1])

        flatlist_time = []
        for item in list(zip(track_list_first_time, track_list_second_time)):
            flatlist_time.append(item[0])
            flatlist_time.append(item[1])

        return flatlist_title, flatlist_time

def gunzip_shutil(source_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as source_file, open(tempfile.NamedTemporaryFile().name, 'wb') as dest_file:
        shutil.copyfileobj(source_file, dest_file, block_size)
        return dest_file.name