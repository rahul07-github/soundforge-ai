"""
Project : SoundForge AI

Module : Frame Generator

Description:
Creates frame timing information based on detected beats.
"""

from backend.app.utils.logger import log_info, log_error


class FrameGenerator:
    """
    Generate frame timing from beat information.
    """

    def __init__(self):
        log_info("FrameGenerator initialized.")

    def generate_frames(self, beat_data: dict) -> list:
        """
        Generate frame sequence using beat timestamps.

        Parameters
        ----------
        beat_data : dict

        Returns
        -------
        list
            List of frame timing dictionaries.
        """

        try:

            beat_times = beat_data["beat_times"]

            frames = []

            for index in range(len(beat_times) - 1):

                start_time = beat_times[index]

                end_time = beat_times[index + 1]

                duration = end_time - start_time

                frame = {

                    "frame_id": index + 1,

                    "start_time": start_time,

                    "end_time": end_time,

                    "duration": duration

                }

                frames.append(frame)

            log_info(
                f"{len(frames)} frames generated successfully."
            )

            return frames

        except Exception as error:

            log_error(f"Frame Generation Failed : {error}")

            raise