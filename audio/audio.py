from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create folders for storing audio and text
os.makedirs("audio", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

# ---------------- Audio Upload ----------------
@app.post("/upload-audio")
async def upload_audio(audio: UploadFile, transcript: str = Form("")):
    audio_path = f"audio/{audio.filename}"
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    # Optional: save transcript as a text file along with audio
    if transcript:
        transcript_path = f"transcripts/{audio.filename.rsplit('.', 1)[0]}.txt"
        with open(transcript_path, "w", encoding="utf-8") as tf:
            tf.write(transcript)

    return {"message": "Audio saved"}

# ---------------- Text Upload ----------------
@app.post("/upload-text")
async def upload_text(
    transcript: str = Form(...),
    filename: str = Form(...)
):
    path = f"transcripts/{filename}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print("Saved transcript:", path)
    print("user text:" , transcript)

    return {
        "message": "Transcript saved",
        "filename": filename,
        "full_transcript": transcript
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

