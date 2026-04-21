# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# # from app.core.config import settings
# # from app.db.database import Base, engine
# from app.api.routes import auth,chatbot

# # Create all tables
# # Base.metadata.create_all(bind=engine)

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from ml_models.pronounciationML.api.routes import router

# app = FastAPI(
#     title="VoxIQ API",
#     description="Multimodal AI for Smarter Communication",
#     version="1.0.0",
# )


# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ── Routers ──
# app.include_router(auth.router)
# app.include_router(chatbot.router)

# @app.get("/")
# def root():
#     return {"message": "VoxIQ API is running 🚀", "version": "1.0.0"}

# import os
# import sys
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse

# # Add parent directory to Python path to allow absolute imports
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from ml_models.emotion_tutor.video_analysis import analyze_video  #.



# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")
# os.makedirs(TEMP_DIR, exist_ok=True)


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

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os, shutil, sys

# Routers
from app.api.routes import auth, chatbot
from ml_models.pronounciationML.api.routes import router as pronunciation_router
from ml_models.emotion_tutor.video_analysis import analyze_video

# Create ONE app
app = FastAPI(
    title="VoxIQ API",
    description="Multimodal AI for Smarter Communication",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(chatbot.router)
app.include_router(pronunciation_router)

# Root
@app.get("/")
def root():
    return {"message": "VoxIQ API is running 🚀"}

# ================= VIDEO UPLOAD =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/upload-video")
async def upload_and_analyze(video: UploadFile = File(...)):
    video_path = os.path.join(TEMP_DIR, video.filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    try:
        result = analyze_video(video_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(video_path)

    return {
        "message": "✅ Video analyzed successfully",
        "analysis": result
    }