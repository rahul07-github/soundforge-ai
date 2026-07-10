
# Module : Smart Frame Generator

import math

from backend.app.utils.logger import log_info, log_error


class FrameGenerator:
    """
    Generate smart frame timings.
    """

    def __init__(self):
        log_info("FrameGenerator initialized.")

    def generate_frames(self, beat_data: dict) -> list:

        try:

            beat_times = beat_data["beat_times"]

            if len(beat_times) < 2:
                raise Exception(
                    "Not enough beats detected."
                )

            ###################################################
            # Configuration
            ###################################################

            SCENE_DURATION = 2.5

            ###################################################
            # Audio Duration
            ###################################################

            total_duration = beat_times[-1]

            total_scenes = max(
                1,
                math.ceil(total_duration / SCENE_DURATION)
            )

            ###################################################
            # Beats Per Scene
            ###################################################

            beats_per_scene = max(
                1,
                math.ceil(len(beat_times) / total_scenes)
            )

            ###################################################
            # Create Scene Frames
            ###################################################

            frames = []

            frame_id = 1

            for index in range(
                0,
                len(beat_times),
                beats_per_scene
            ):

                start_time = beat_times[index]

                if index + beats_per_scene < len(beat_times):

                    end_time = beat_times[
                        index + beats_per_scene
                    ]

                else:

                    end_time = beat_times[-1]

                duration = end_time - start_time

                frames.append(
                    {
                        "frame_id": frame_id,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": duration
                    }
                )

                frame_id += 1

            ###################################################

            log_info(
                f"{len(frames)} smart frames generated."
            )

            return frames

        except Exception as error:

            log_error(
                f"Frame Generation Failed : {error}"
            )

            raise