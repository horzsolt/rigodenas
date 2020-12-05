from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import time
from loghelper import logger
from mailer import send_plaintext_mail

def get_audio_info(path):

    try:
        audio = MP3(path)
        length_minutes = time.gmtime(audio.info.length).tm_min
        bitrate = audio.info.bitrate/1000
        return length_minutes, bitrate
    except Exception as ex:
        logger.error(f"error get_audio_info of {path}")
        send_plaintext_mail(f"error get_audio_info of {path}")
        logger.error(ex, exc_info=True)
