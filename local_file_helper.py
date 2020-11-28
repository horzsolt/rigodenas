import os
from mp3helper import get_audio_info
import shutil
from m3u import generate_m3u
from loghelper import logger

def clean_download_directory(directory):

    logger.debug(f"Cleaning directory: {directory}")

    for filename in os.listdir(directory):
        fullpath = os.path.join(directory,filename)
        if (os.path.isfile(fullpath)):
            if (filename.endswith('.mp3')):
                length_minutes, bitrate = get_audio_info(fullpath)
                if (length_minutes > 25) or (length_minutes < 4) or (bitrate < 192):
                    os.remove(fullpath)
        else:
            clean_download_directory(fullpath)

    if not [f for f in os.listdir(directory) if f.endswith('.mp3')]:
        shutil.rmtree(directory)
    else:
        generate_m3u(directory)