# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import os, shutil, sys

# # Routers
# from app.api.routes import auth, chatbot
# from ml_models.pronounciationML.api.routes import router as pronunciation_router
# from ml_models.emotion_tutor.video_analysis import analyze_video

# # Create ONE app
# app = FastAPI(
#     title="VoxIQ API",
#     description="Multimodal AI for Smarter Communication",
#     version="1.0.0",
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5501"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include all routers
# app.include_router(auth.router)
# app.include_router(chatbot.router)
# app.include_router(pronunciation_router)

# # Root
# @app.get("/")
# def root():
#     return {"message": "VoxIQ API is running 🚀"}

# # ================= VIDEO UPLOAD =================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")
# os.makedirs(TEMP_DIR, exist_ok=True)

# @app.post("/upload-video")
# async def upload_and_analyze(video: UploadFile = File(...)):
#     video_path = os.path.join(TEMP_DIR, video.filename)

#     with open(video_path, "wb") as buffer:
#         shutil.copyfileobj(video.file, buffer)

#     try:
#         result = analyze_video(video_path)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#     finally:
#         os.remove(video_path)

#     return {
#         "message": "✅ Video analyzed successfully",
#         "analysis": result
#     }




import uuid
import os
import shutil
import sys

print("===== STARTING APP =====")

print("1 - Importing FastAPI")
from fastapi import FastAPI, Form, UploadFile, File

print("2 - Importing CORS")
from fastapi.middleware.cors import CORSMiddleware

print("3 - Importing JSONResponse")
from fastapi.responses import JSONResponse

print("4 - Importing auth router")
from app.api.routes import auth

print("5 - Importing chatbot router")
from app.api.routes import chatbot

print("6 - Importing pronunciation router")
from ml_models.pronounciationML.api.routes import router as pronunciation_router

print("7 - Importing video analysis")
from ml_models.emotion_tutor.video_analysis import analyze_video

print("8 - Importing pronunciation logic")
from ml_models.pronounciationML.api.routes import evaluate_pronunciation_logic

print("9 - All imports completed")

app = FastAPI(
    title="VoxIQ API",
    description="Multimodal AI for Smarter Communication",
    version="1.0.0",
)

print("10 - FastAPI app created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("11 - CORS configured")

app.include_router(auth.router)
print("12 - Auth router added")

app.include_router(chatbot.router)
print("13 - Chatbot router added")

app.include_router(pronunciation_router)
print("14 - Pronunciation router added")


@app.get("/")
def root():
    print("ROOT ENDPOINT CALLED")
    return {"message": "VoxIQ API is running 🚀"}


print("15 - Root endpoint created")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")
os.makedirs(TEMP_DIR, exist_ok=True)

print("16 - Temp directory created")

print("===== APP INITIALIZATION COMPLETE =====")
