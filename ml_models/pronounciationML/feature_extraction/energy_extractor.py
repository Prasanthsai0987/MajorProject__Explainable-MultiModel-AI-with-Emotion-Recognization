import librosa
import numpy as np

def extract_energy(audio):
    energy = librosa.feature.rms(y=audio)
    return float(np.mean(energy))


# 👉 RMS = Root Mean Square  .(Loudness)