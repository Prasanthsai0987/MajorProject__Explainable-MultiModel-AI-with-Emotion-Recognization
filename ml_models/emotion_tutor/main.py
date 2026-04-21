import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# Add parent directory to Python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from emotion_tutor.video_analysis import analyze_video  #.

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_videos")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.post("/upload-video")
async def upload_and_analyze(video: UploadFile = File(...)):
    video_path = os.path.join(TEMP_DIR, video.filename)

    # Save video
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    try:
        result = analyze_video(video_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(video_path)  # cleanup

    return {
        "message": "✅ Video analyzed successfully",
        "analysis": result
    }
