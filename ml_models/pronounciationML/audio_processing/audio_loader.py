import librosa

def load_audio(path):
    audio, sr = librosa.load(path, sr=16000)
    return audio, sr


# 👉 sr = sample rate, which tells how many audio samples are captured per second.