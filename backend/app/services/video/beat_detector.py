"""
Project : SoundForge AI

Module : Beat Detector

Description:
Detects BPM and beat timestamps from the generated song.
"""

import traceback
import librosa
import numpy as np

from backend.app.utils.logger import log_info, log_error


class BeatDetector:
    """
    Detect beats and tempo from an audio file.
    """

    def __init__(self):
        log_info("BeatDetector initialized.")

    def detect_beats(self, song_path: str) -> dict:
        """
        Detect beats from the given audio file.
        """

        try:
            log_info(f"Loading audio : {song_path}")

            # -----------------------------
            # Load Audio
            # -----------------------------
            audio, sample_rate = librosa.load(
                song_path,
                sr=None
            )

            print("\n" + "=" * 60)
            print("DEBUG : AUDIO INFORMATION")
            print("=" * 60)
            print(f"Song Path   : {song_path}")
            print(f"Sample Rate : {sample_rate}")
            print(f"Audio Shape : {audio.shape}")
            print(f"Audio Length: {len(audio)} samples")
            print(f"Duration    : {len(audio) / sample_rate:.2f} sec")
            print("=" * 60 + "\n")

            # -----------------------------
            # Beat Detection
            # -----------------------------
            tempo, beat_frames = librosa.beat.beat_track(
                y=audio,
                sr=sample_rate
            )

            beat_times = librosa.frames_to_time(
                beat_frames,
                sr=sample_rate
            )

            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0])
            else:
                tempo = float(tempo)

            log_info(f"Beat Detection Completed | BPM : {tempo:.2f}")

            print("\n" + "=" * 60)
            print("DEBUG : BEAT INFORMATION")
            print("=" * 60)
            print(f"BPM         : {tempo:.2f}")
            print(f"Total Beats : {len(beat_frames)}")
            print(f"First Beats : {beat_times[:10]}")
            print("=" * 60 + "\n")

            return {
                "tempo": tempo,
                "beat_frames": beat_frames.tolist(),
                "beat_times": beat_times.tolist()
            }

        except Exception as error:

            log_error(f"Beat Detection Failed : {repr(error)}")

            print("\n" + "=" * 60)
            print("FULL TRACEBACK")
            print("=" * 60)
            traceback.print_exc()
            print("=" * 60 + "\n")

            raise