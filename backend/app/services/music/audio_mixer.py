"""
audio_mixer.py

Called as: mix_audio(matched_vocal_path, beat_path, song_path)
"""

import os
from pydub import AudioSegment


def mix_audio(
    vocal_path: str,
    beat_path: str,
    output_path: str,
    vocal_gain_db: float = 3.0,
    beat_gain_db: float = -4.0,
) -> str:
    if not os.path.exists(beat_path):
        raise FileNotFoundError(f"Beat not found: {beat_path}")
    if not os.path.exists(vocal_path):
        raise FileNotFoundError(f"Vocal not found: {vocal_path}")

    vocal = AudioSegment.from_file(vocal_path) + vocal_gain_db
    beat = AudioSegment.from_file(beat_path) + beat_gain_db

    if len(beat) < len(vocal):
        loops_needed = (len(vocal) // len(beat)) + 1
        beat = beat * loops_needed
    beat = beat[: len(vocal)]

    mixed = beat.overlay(vocal)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    mixed.export(output_path, format="mp3", bitrate="192k")

    print(f"[audio_mixer] Final song saved: {output_path}")
    return output_path