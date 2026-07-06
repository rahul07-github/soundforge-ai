"""
Project: SoundForge AI

Module: Validators
"""

from pathlib import Path

from backend.app.utils.constants import (
    SUPPORTED_AUDIO_FORMATS,
    SUPPORTED_IMAGE_FORMATS
)


def file_exists(file_path: str) -> bool:
    """
    Check whether file exists.
    """
    return Path(file_path).exists()


def is_valid_audio(file_path: str) -> bool:
    """
    Validate audio file extension.
    """
    return Path(file_path).suffix.lower() in SUPPORTED_AUDIO_FORMATS


def is_valid_image(file_path: str) -> bool:
    """
    Validate image extension.
    """
    return Path(file_path).suffix.lower() in SUPPORTED_IMAGE_FORMATS


def validate_audio(file_path: str):

    if not file_exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    if not is_valid_audio(file_path):
        raise ValueError("Unsupported audio format.")


def validate_image(file_path: str):

    if not file_exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    if not is_valid_image(file_path):
        raise ValueError("Unsupported image format.")