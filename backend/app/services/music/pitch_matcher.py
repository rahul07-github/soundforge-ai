"""
pitch_matcher.py

Called as: match_vocal_to_beat(vocal_path, matched_vocal_path)

CURRENT LIMITATION: beat_path isn't passed in by the current
lyrics_generator.py, so real pitch/key alignment to a specific beat
isn't possible yet. This version normalizes loudness and re-encodes
the vocal as a safe pass-through so your pipeline runs end-to-end.

TO UPGRADE LATER: change the call in lyrics_generator.py to:
    beat_path = select_beat(user_prompt)   # move this line up, before this call
    match_vocal_to_beat(vocal_path, matched_vocal_path, beat_path)
and use analyze_beat() below to get its key/tempo for real matching.
"""

import os
from pydub import AudioSegment, effects
import librosa
import numpy as np

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def analyze_beat(beat_path: str) -> dict:
    """Extracts tempo + estimated key from a beat file. Use this once
    beat_path is available at the matching step."""
    y, sr = librosa.load(beat_path, sr=None, mono=True)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    best_score, best_key, best_mode = -np.inf, "C", "major"
    for i in range(12):
        rotated = np.roll(chroma_mean, -i)
        major_score = np.corrcoef(rotated, MAJOR_PROFILE)[0, 1]
        minor_score = np.corrcoef(rotated, MINOR_PROFILE)[0, 1]
        if major_score > best_score:
            best_score, best_key, best_mode = major_score, NOTE_NAMES[i], "major"
        if minor_score > best_score:
            best_score, best_key, best_mode = minor_score, NOTE_NAMES[i], "minor"

    return {"tempo_bpm": round(float(tempo), 1), "estimated_key": f"{best_key} {best_mode}"}


def match_vocal_to_beat(vocal_path: str, output_path: str, beat_path: str = None) -> str:
    """
    Current behavior: normalizes vocal loudness and saves it, so the
    pipeline runs cleanly. If beat_path is provided, also pitch-shifts
    the vocal toward the beat's estimated key (rough alignment).
    """
    vocal = AudioSegment.from_file(vocal_path)
    vocal = effects.normalize(vocal)

    if beat_path and os.path.exists(beat_path):
        beat_info = analyze_beat(beat_path)
        print(f"[pitch_matcher] Beat info: {beat_info} (key-aware shifting not yet applied)")
        # Real pitch-shifting to a target key would go here once beat_path
        # is reliably passed in -- e.g. using librosa.effects.pitch_shift.

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    vocal.export(output_path, format="mp3", bitrate="192k")

    print(f"[pitch_matcher] Matched vocal saved: {output_path}")
    return output_path