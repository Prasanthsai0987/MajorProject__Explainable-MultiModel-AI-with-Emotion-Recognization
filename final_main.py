import os
import sys
import shutil
import subprocess
import uuid

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

# Ensure project root (backend/) is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Database
from app.db.database import Base, engine
from app.db import models

# Routers
from app.api.routes import auth, chatbot

from ml_models.pronounciationML.api.routes import (
    router as pronunciation_router,
    evaluate_pronunciation_logic,
)

# Video analysis
from ml_models.emotion_tutor.video_analysis import analyze_video


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="VoxIQ API",
    description="Multimodal AI for Smarter Communication",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://major-project-explainable-multi-mod.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE STARTUP
# ============================================================

@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables initialized")
    except Exception as e:
        print("❌ Database initialization failed:", e)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth.router)
app.include_router(chatbot.router)
app.include_router(pronunciation_router)


# ============================================================
# TEMP DIRECTORY
# ============================================================

TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")

os.makedirs(TEMP_DIR, exist_ok=True)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "VoxIQ API is running 🚀"
    }


# ============================================================
# AUDIO EXTRACTION
# ============================================================

def extract_audio(video_path, audio_path):
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vn",
        "-acodec",
        "mp3",
        audio_path,
    ]

    subprocess.run(command, check=True)


# ============================================================
# VIDEO ANALYSIS
# ============================================================

@app.post("/upload-video")
async def upload_and_analyze(
    video: UploadFile = File(...)
):
    video_path = os.path.join(
        TEMP_DIR,
        video.filename
    )

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(
            video.file,
            buffer
        )

    try:
        result = analyze_video(video_path)

        return {
            "message": "Video analyzed successfully",
            "analysis": result,
        }

    except Exception as e:
        print("Video Analysis Error:", e)

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            },
        )

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)


# ============================================================
# FULL SESSION ANALYSIS
# ============================================================

@app.post("/analyze-session")
async def analyze_session(
    video: UploadFile = File(...),
    transcript: str = Form(...)
):
    video_filename = f"{uuid.uuid4()}.webm"
    audio_filename = f"{uuid.uuid4()}.mp3"

    video_path = os.path.join(
        TEMP_DIR,
        video_filename
    )

    audio_path = os.path.join(
        TEMP_DIR,
        audio_filename
    )

    try:
        # Save video
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(
                video.file,
                buffer
            )

        # Extract audio
        extract_audio(
            video_path,
            audio_path
        )

        # Analyze video
        video_result = analyze_video(
            video_path
        )

        # Analyze speech
        pronunciation_result = (
            evaluate_pronunciation_logic(
                audio_path,
                transcript
            )
        )

        return {
            "message": "Full session analyzed",
            "video_analysis": video_result,
            "speech_analysis": pronunciation_result,
        }

    except Exception as e:
        print("Session Error:", e)

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            },
        )

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

        if os.path.exists(audio_path):
            os.remove(audio_path)


# ============================================================
# DATABASE TEST
# ============================================================

@app.get("/api/db-test")
def db_test():

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            return {
                "database": "connected",
                "result": result.scalar(),
            }

    except Exception as e:

        print("Database test failed:", e)

        return {
            "database": "failed",
            "error": str(e),
        }