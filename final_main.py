# # from fastapi import FastAPI, UploadFile, File
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import JSONResponse
# # import os, shutil, sys

# # # Routers
# # from app.api.routes import auth, chatbot
# # from ml_models.pronounciationML.api.routes import router as pronunciation_router
# # from ml_models.emotion_tutor.video_analysis import analyze_video

# # # Create ONE app
# # app = FastAPI(
# #     title="VoxIQ API",
# #     description="Multimodal AI for Smarter Communication",
# #     version="1.0.0",
# # )

# # # CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=[
# #         "http://localhost:5173",
# #         "http://127.0.0.1:5501"
# #     ],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Include all routers
# # app.include_router(auth.router)
# # app.include_router(chatbot.router)
# # app.include_router(pronunciation_router)

# # # Root
# # @app.get("/")
# # def root():
# #     return {"message": "VoxIQ API is running 🚀"}

# # # ================= VIDEO UPLOAD =================
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")
# # os.makedirs(TEMP_DIR, exist_ok=True)

# # @app.post("/upload-video")
# # async def upload_and_analyze(video: UploadFile = File(...)):
# #     video_path = os.path.join(TEMP_DIR, video.filename)

# #     with open(video_path, "wb") as buffer:
# #         shutil.copyfileobj(video.file, buffer)

# #     try:
# #         result = analyze_video(video_path)
# #     except Exception as e:
# #         return JSONResponse(status_code=500, content={"error": str(e)})
# #     finally:
# #         os.remove(video_path)

# #     return {
# #         "message": "✅ Video analyzed successfully",
# #         "analysis": result
# #     }





<<<<<<< HEAD
import os
import shutil
import subprocess
from fastapi import Form
=======
# @app.post("/upload-video")
# async def upload_and_analyze(video: UploadFile = File(...)):
#     video_path = os.path.join(TEMP_DIR, video.filename)

#     # Save video
#     with open(video_path, "wb") as buffer:
#         shutil.copyfileobj(video.file, buffer)

#     try:
#         result = analyze_video(video_path)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#     finally:
#         os.remove(video_path)  # cleanup

#     return {
#         "message": "✅ Video analyzed successfully",
#         "analysis": result
#     }



# # CORS setup (for frontend connection)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5501"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(router)
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
import uuid

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure project root (backend/) is on sys.path so imports like `app.*` work when running locally.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Routers
from app.api.routes import auth, chatbot
from ml_models.pronounciationML.api.routes import (
    router as pronunciation_router,
    evaluate_pronunciation_logic
)

# Video analysis
from ml_models.emotion_tutor.video_analysis import analyze_video
from ml_models.pronounciationML.api.routes import evaluate_pronunciation_logic

# ------------------- FASTAPI APP -------------------

app = FastAPI(
    title="VoxIQ API",
    description="Multimodal AI for Smarter Communication",
    version="1.0.0",
)

# ------------------- CORS -------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    
        "http://localhost:5173",
<<<<<<< HEAD
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
=======
        "http://localhost:5174",   # ✅ ADD THIS
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://major-project-explainable-multi-mod.vercel.app"
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- ROUTERS -------------------

app.include_router(auth.router)
app.include_router(chatbot.router)
app.include_router(pronunciation_router)

# ------------------- TEMP DIRECTORY -------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")

os.makedirs(TEMP_DIR, exist_ok=True)

# ------------------- ROOT -------------------

@app.get("/")
def root():
    return {
        "message": "VoxIQ API is running 🚀"
    }

# ------------------- AUDIO EXTRACTION -------------------

def extract_audio(video_path, audio_path):
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "mp3",
        audio_path
    ]

    subprocess.run(command, check=True)
# ------------------- VIDEO ANALYSIS -------------------

@app.post("/upload-video")
async def upload_and_analyze(video: UploadFile = File(...)):
    video_path = os.path.join(TEMP_DIR, video.filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    try:
        result = analyze_video(video_path)

<<<<<<< HEAD
        return {
            "message": "Video analyzed successfully",
            "analysis": result
        }

    except Exception as e:
        print("Video Analysis Error:", e)

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
=======
    return {
        "message": "✅ Video analyzed successfully",
        "analysis": result
    }
    
import subprocess

def extract_audio(video_path, audio_path):
    command = [
        r"C:\ffmpeg\bin\ffmpeg.exe",   
        "-i", video_path,
        "-vn",
        "-acodec", "mp3",
        audio_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(result.stderr)  
        
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
@app.post("/analyze-session")
async def analyze_session(
    video: UploadFile = File(...),
    transcript: str = Form(...)
):
<<<<<<< HEAD
=======
    # unique filenames
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
    video_filename = f"{uuid.uuid4()}.webm"
    audio_filename = f"{uuid.uuid4()}.mp3"

    video_path = os.path.join(TEMP_DIR, video_filename)
    audio_path = os.path.join(TEMP_DIR, audio_filename)

    try:
<<<<<<< HEAD
        # Save video
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # Extract audio using FFmpeg
        extract_audio(video_path, audio_path)

        # Run ML models
=======
        # 🎥 Save video
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # 🎤 Extract audio from video
        extract_audio(video_path, audio_path)

        # 🧠 Run models
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
        video_result = analyze_video(video_path)
        pronunciation_result = evaluate_pronunciation_logic(audio_path, transcript)

        return {
<<<<<<< HEAD
            "message": "Full session analyzed",
=======
            "message": "✅ Full session analyzed",
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
            "video_analysis": video_result,
            "speech_analysis": pronunciation_result
        }

    except Exception as e:
<<<<<<< HEAD
        print("Session Error:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
=======
        print("❌ ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
>>>>>>> 0eac9bd (Update backend deployment and production configuration)

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
<<<<<<< HEAD

        if os.path.exists(audio_path):
            os.remove(audio_path)






=======
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        
>>>>>>> 0eac9bd (Update backend deployment and production configuration)
