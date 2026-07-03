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



import subprocess

@app.get("/ffmpeg-check")
def ffmpeg_check():
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        return {"installed": True, "output": result.stdout.splitlines()[0]}
    except Exception as e:
        return {"installed": False, "error": str(e)}


