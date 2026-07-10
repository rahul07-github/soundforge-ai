<<<<<<< HEAD
from pathlib import Path
from pydub import AudioSegment

AudioSegment.converter = r"E:\ffmpeg2\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"E:\ffmpeg2\bin\ffprobe.exe"


def mix_audio(vocal_path: str, beat_path: str, output_path: str):

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    vocal = AudioSegment.from_mp3(vocal_path)
    beat = AudioSegment.from_mp3(beat_path)

    # Increase beat volume
    beat -= 4

    # Reduce vocal volume slightly
    vocal += 8

    # Extend beat if shorter
    while len(beat) < len(vocal):
        beat += beat

    beat = beat[:len(vocal)]

    final = beat.overlay(vocal)

    # Limit demo to 20 seconds
    final = final[:20000]

    final.export(output_path, format="mp3")

=======
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
>>>>>>> origin
    return output_path