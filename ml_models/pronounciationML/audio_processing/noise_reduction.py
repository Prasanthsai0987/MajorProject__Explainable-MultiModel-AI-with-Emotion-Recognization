import noisereduce as nr

def reduce_noise(audio, sr):
    cleaned = nr.reduce_noise(y=audio, sr=sr)
    return cleaned