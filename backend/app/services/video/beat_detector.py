"""
Project : SoundForge AI

Module : Beat Detector

Description:
Detects BPM and beat timestamps from the generated song.
"""

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

        Parameters
        ----------
        song_path : str
            Path to the generated MP3 file.

        Returns
        -------
        dict
            tempo
            beat_frames
            beat_times
        """

        try:

            log_info(f"Loading audio : {song_path}")

            # ---------------------------------------------
            # Load Audio
            # ---------------------------------------------

            audio, sample_rate = librosa.load(
                song_path,
                sr=None
            )

            # ---------------------------------------------
            # Beat Tracking
            # ---------------------------------------------

            tempo, beat_frames = librosa.beat.beat_track(
                y=audio,
                sr=sample_rate
            )

            # ---------------------------------------------
            # Convert Frame → Time
            # ---------------------------------------------

            beat_times = librosa.frames_to_time(
                beat_frames,
                sr=sample_rate
            )
            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0])
            else:
                tempo = float(tempo)

            log_info(
                f"Beat Detection Completed | BPM : {tempo:.2f}"
            )


            return {

                "tempo": tempo,

                "beat_frames": beat_frames.tolist(),

                "beat_times": beat_times.tolist()

            }

        except Exception as error:

            log_error(f"Beat Detection Failed : {error}")

            raise