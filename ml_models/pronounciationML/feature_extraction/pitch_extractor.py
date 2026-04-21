import librosa
import numpy as np

def extract_pitch(audio, sr):
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    pitch = np.mean(pitches)
    return float(pitch)

# sr = sample rate
# /➡ How high or low a voice is tells about the pitch 