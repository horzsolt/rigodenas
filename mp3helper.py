from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import time

def get_audio_info(path):

    audio = MP3(path)
    length_minutes = time.gmtime(audio.info.length).tm_min
    bitrate = audio.info.bitrate/1000

    return length_minutes, bitrate
