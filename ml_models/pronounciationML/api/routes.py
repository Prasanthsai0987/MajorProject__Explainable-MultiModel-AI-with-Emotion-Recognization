from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import nltk
nltk.data.path.append('C:/nltk_data')
# natural language toolkit


from ml_models.pronounciationML.audio_processing.audio_loader import load_audio
from ml_models.pronounciationML.feature_extraction.pitch_extractor import extract_pitch
from ml_models.pronounciationML.feature_extraction.mfcc_extractor import extract_mfcc
from ml_models.pronounciationML.feature_extraction.energy_extractor import extract_energy
from ml_models.pronounciationML.speech_processing.phoneme_extractor import text_to_phonemes
from ml_models.pronounciationML.pronunciation_scoring.phoneme_alignment import compare_phonemes
from ml_models.pronounciationML.pronunciation_scoring.score_calculator import calculate_score
from ml_models.pronounciationML.feedback.feedback_generator import generate_feedback

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- MAIN PRONUNCIATION API ----------------
@router.post("/evaluate")
async def evaluate_pronunciation(
        audio: UploadFile = File(...),
        transcript: str = Form(...)
):

    # 1️⃣ Save audio
    filepath = f"{UPLOAD_FOLDER}/{audio.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    print("Audio saved:", filepath)
    print("Transcript:", transcript)

    # 2️⃣ Load audio
    audio_data, sr = load_audio(filepath)

    # 3️⃣ Feature extraction
    pitch = extract_pitch(audio_data, sr)
    mfcc = extract_mfcc(audio_data, sr)
    energy = extract_energy(audio_data)

    # 4️⃣ Phoneme conversion
    expected_phonemes = text_to_phonemes(transcript)

    spoken_phonemes = text_to_phonemes(transcript)

    # 5️⃣ Compare phonemes
    phoneme_score = compare_phonemes(expected_phonemes, spoken_phonemes)

    # 6️⃣ Final score
    score = calculate_score(pitch, mfcc, energy, phoneme_score)

    # 7️⃣ Feedback
    feedback = generate_feedback(score)

    return {
        "score": score,
        "pitch": pitch,
        "mfcc": mfcc,
        "energy": energy,
        "phoneme_score": phoneme_score,
        "feedback": feedback
    }