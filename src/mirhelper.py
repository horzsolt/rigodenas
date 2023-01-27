import librosa
import numpy

#https://librosa.org/doc/latest/tutorial.html
def get_beat(path):
    data, sr = librosa.load(r'q:\!mix\2020_10\10A - 126 - John Summit - Deep End Extended Mix_pn.mp3', sr=None)
    data_harmonic, data_percussive = librosa.effects.hpss(data)
    tempo, beat_frames = librosa.beat.beat_track(y=data, sr=sr)
    mfcc = librosa.feature.mfcc(y=data, sr=sr, hop_length=512, n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc)
    beat_mfcc_delta = librosa.util.sync(numpy.vstack([mfcc, mfcc_delta]), beat_frames)
    chromagram = librosa.feature.chroma_cqt(y=data_harmonic, sr=sr)

    beat_chroma = librosa.util.sync(chromagram, beat_frames, aggregate=numpy.median)
    beat_features = numpy.vstack([beat_chroma, beat_mfcc_delta])

    print(tempo)
    print('--------')
    print(beat_features)
    print('--------')    
    print(mfcc)
    print('--------')    
    print(mfcc_delta)
    print('--------')    
    print(beat_mfcc_delta)
    print('--------')    
    print(chromagram)