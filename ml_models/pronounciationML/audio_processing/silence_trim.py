import librosa

def trim_silence(audio):
    trimmed, _ = librosa.effects.trim(audio)
    return trimmed