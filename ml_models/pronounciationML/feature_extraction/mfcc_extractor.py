import librosa
import numpy as np

def extract_mfcc(audio, sr):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return float(np.mean(mfcc))

# 👉 MFCC = Mel-Frequency Cepstral Coefficients



# 🧠 How humans perceive sound (especially speech)


# and it converts to 12.3, -4.5 ....