"""
Project: SoundForge AI

Module: backend/app/utils/constants.py
"""
from pathlib import Path


# Video Configuration

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080

FPS = 30

DEFAULT_VIDEO_FORMAT = "mp4"

VIDEO_CODEC = "libx264"


# Thumbnail Configuration

THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720

THUMBNAIL_FORMAT = "png"


# ==========================================
# Audio Configuration
# ==========================================

DEFAULT_AUDIO_FORMAT = "mp3"

SUPPORTED_AUDIO_FORMATS = [
    ".mp3",
    ".wav"
]


# ==========================================
# Image Configuration
# ==========================================

SUPPORTED_IMAGE_FORMATS = [
    ".png",
    ".jpg",
    ".jpeg"
]

# Base Directory ==============


BASE_DIR = Path(__file__).resolve().parents[1]

STORAGE_DIR = BASE_DIR / "storage"

# Storage Paths ===============

UPLOAD_FOLDER = STORAGE_DIR / "uploads"

GENERATED_FOLDER = STORAGE_DIR / "generated"

VIDEO_FOLDER = GENERATED_FOLDER / "videos"

THUMBNAIL_FOLDER = GENERATED_FOLDER / "thumbnails"

TEMP_FOLDER = STORAGE_DIR / "temp"

EXPORT_FOLDER = STORAGE_DIR / "exports"

SONGS_FOLDER = GENERATED_FOLDER / "songs"

LYRICS_FOLDER = GENERATED_FOLDER / "lyrics"

COVERS_FOLDER = GENERATED_FOLDER / "covers"

METADATA_FOLDER = GENERATED_FOLDER / "metadata"

SUBTITLE_FOLDER = GENERATED_FOLDER / "subtitles"


# ==========================================
# Logging
# ==========================================

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


# ==========================================
# Default Values
# ==========================================

DEFAULT_FRAME_DURATION = 0.5

DEFAULT_TRANSITION = "fade"

DEFAULT_QUALITY = "high"