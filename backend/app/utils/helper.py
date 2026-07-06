"""
Project: SoundForge AI

Module: Helper Functions

Description:
Common helper functions used across the Video Module.
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime


def generate_unique_id() -> str:
    """
    Generate a unique ID for songs, videos, thumbnails, etc.
    """
    return str(uuid4())


def get_current_timestamp() -> str:
    """
    Return current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_output_filename(prefix: str, extension: str) -> str:
    """
    Example:
        build_output_filename("video", "mp4")
        -> video_ab12cd34.mp4
    """
    unique_id = generate_unique_id()[:8]
    return f"{prefix}_{unique_id}.{extension}"


def build_path(folder: str, filename: str) -> Path:
    """
    Build a complete file path.
    """
    return Path(folder) / filename


def seconds_to_mmss(seconds: float) -> str:
    """
    Convert seconds into MM:SS format.
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02}:{seconds:02}"