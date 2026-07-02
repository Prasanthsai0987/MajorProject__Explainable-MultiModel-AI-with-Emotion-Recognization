print("1. routes.py started")

from fastapi import APIRouter
print("2. FastAPI imported")

import os
import nltk

print("3. nltk imported")

nltk.data.path.append("C:/nltk_data")

print("4. importing audio_loader")
from ml_models.pronounciationML.audio_processing.audio_loader import load_audio

print("5. importing pitch")
from ml_models.pronounciationML.feature_extraction.pitch_extractor import extract_pitch

print("6. importing mfcc")
from ml_models.pronounciationML.feature_extraction.mfcc_extractor import extract_mfcc

print("7. importing energy")
from ml_models.pronounciationML.feature_extraction.energy_extractor import extract_energy

print("8. importing phoneme")
from ml_models.pronounciationML.speech_processing.phoneme_extractor import text_to_phonemes

print("9. importing alignment")
from ml_models.pronounciationML.pronunciation_scoring.phoneme_alignment import compare_phonemes

print("10. importing score")
from ml_models.pronounciationML.pronunciation_scoring.score_calculator import calculate_score

print("11. importing feedback")
from ml_models.pronounciationML.feedback.feedback_generator import generate_feedback

print("12. creating router")

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("13. defining function")


def evaluate_pronunciation_logic(filepath, transcript):

    audio_data, sr = load_audio(filepath)

    pitch = extract_pitch(audio_data, sr)
    mfcc = extract_mfcc(audio_data, sr)
    energy = extract_energy(audio_data)

    expected_phonemes = text_to_phonemes(transcript)
    spoken_phonemes = text_to_phonemes(transcript)

    phoneme_score = compare_phonemes(
        expected_phonemes,
        spoken_phonemes
    )

    score = calculate_score(
        pitch,
        mfcc,
        energy,
        phoneme_score
    )

    feedback = generate_feedback(score)

    return {
        "score": score,
        "pitch": pitch,
        "mfcc": mfcc,
        "energy": energy,
        "phoneme_score": phoneme_score,
        "feedback": feedback,
    }

print("14. function created successfully")
