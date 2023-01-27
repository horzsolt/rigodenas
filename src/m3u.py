import os
from loghelper import logger

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            name, ext = os.path.splitext(file)
            if ext == (".mp3"):
                yield file

def generate_m3u(directory):
    try:
        fullPath = os.path.join(directory, "!generated.m3u")
        if(os.path.exists(fullPath)):
            os.remove(fullPath)
        
        m3u = open(fullPath, "x")
        try:
            for file in files(directory):
                m3u.write(str(file) + "\n")
        finally:
            m3u.close()
    except Exception as ex:
        logger.error(ex, exc_info=True)
