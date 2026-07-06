#  video.py sirf ye kaam karega: ----
# Receive Request, Validate Input, Call Pipeline, Return Response, Handle Exceptions

# Import libraries ----

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

from backend.app.services.video.pipeline import VideoPipeline
from backend.app.utils.logger import log_info, log_error
from backend.app.utils.constants import METADATA_FOLDER


# Router -----
router = APIRouter(
    prefix="/video",
    tags=["Video"]
)

# Request Schema ---
class VideoRequest(BaseModel):
    song_id: str

# Response Schema
class VideoResponse(BaseModel):
    success: bool
    message: str
    song_id: str
    video_path: str
    thumbnail_path: str
    subtitle_path: str

# Create Pipeline ------
pipeline = VideoPipeline()

# POST/generate-video ----
@router.post("/generate", response_model=VideoResponse)
def generate_video(request: VideoRequest):

    try:

        log_info(f"Generating video for {request.song_id}")

        result = pipeline.generate_video(
            request.song_id
        )

        return VideoResponse(
            success=True,
            message="Video generated successfully.",
            song_id=result["song_id"],

            video_path=result["video_path"],

            thumbnail_path=result["thumbnail_path"],

            subtitle_path=result["subtitle_path"]
        )

    except Exception as e:

        log_error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Get Video Status ---
@router.get("/status/{song_id}")
def get_status(song_id: str):

    metadata_file = METADATA_FOLDER / f"{song_id}.json"

    if not metadata_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Metadata not found."
        )

    with open(
        metadata_file,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    return metadata

# Download Endpoint -------
@router.get("/download/{song_id}")
def download_video(song_id: str):

    return {
        "song_id": song_id,
        "message": "Download endpoint."
    }