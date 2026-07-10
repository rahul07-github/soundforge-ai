<<<<<<< HEAD
"""
Project : SoundForge AI

Module : Smart Frame Generator

Description:
Generate intelligent frame timeline from beat detection.
"""

import math
import random
=======

# Module : Smart Frame Generator

import math
>>>>>>> origin

from backend.app.utils.logger import log_info, log_error


class FrameGenerator:
    """
<<<<<<< HEAD
    Generate smart cinematic frame timings.
    """

    def __init__(self):

        log_info("FrameGenerator initialized.")

        ###################################################
        # Available camera motions
        ###################################################

        self.motions = [

            "zoom_in",
            "zoom_out",
            "pan_left",
            "pan_right",
            "pan_up",
            "pan_down",
            "diagonal_left",
            "diagonal_right"

        ]

        ###################################################
        # Available transitions
        ###################################################

        self.transitions = [

            "crossfade",
            "fade",
            "zoom"

        ]

=======
    Generate smart frame timings.
    """

    def __init__(self):
        log_info("FrameGenerator initialized.")

>>>>>>> origin
    def generate_frames(self, beat_data: dict) -> list:

        try:

            beat_times = beat_data["beat_times"]
<<<<<<< HEAD
            tempo = beat_data["tempo"]

            if len(beat_times) < 2:

=======

            if len(beat_times) < 2:
>>>>>>> origin
                raise Exception(
                    "Not enough beats detected."
                )

            ###################################################
<<<<<<< HEAD
            # Dynamic scene duration based on BPM
            ###################################################

            if tempo < 90:

                scene_duration = 2.5

            elif tempo < 120:

                scene_duration = 1.8

            elif tempo < 150:

                scene_duration = 1.3

            else:

                scene_duration = 1.0

            min_duration = 0.8

            ###################################################
            # Total scenes
=======
            # Configuration
            ###################################################

            SCENE_DURATION = 2.5

            ###################################################
            # Audio Duration
>>>>>>> origin
            ###################################################

            total_duration = beat_times[-1]

            total_scenes = max(
<<<<<<< HEAD

                1,

                math.ceil(
                    total_duration / scene_duration
                )

            )

            beats_per_scene = max(

                1,

                math.ceil(
                    len(beat_times) / total_scenes
                )

            )

            ###################################################
            # Generate timeline
=======
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
>>>>>>> origin
            ###################################################

            frames = []

            frame_id = 1

            for index in range(
<<<<<<< HEAD

                0,

                len(beat_times),

                beats_per_scene

=======
                0,
                len(beat_times),
                beats_per_scene
>>>>>>> origin
            ):

                start_time = beat_times[index]

                if index + beats_per_scene < len(beat_times):

                    end_time = beat_times[
                        index + beats_per_scene
                    ]

                else:

                    end_time = beat_times[-1]

                duration = end_time - start_time

<<<<<<< HEAD
                ###################################################
                # Merge very short scenes
                ###################################################

                if duration < min_duration and frames:

                    frames[-1]["end_time"] = end_time

                    frames[-1]["duration"] = (

                        end_time -

                        frames[-1]["start_time"]

                    )

                    continue

                ###################################################
                # Scene metadata
                ###################################################

                frames.append(

                    {

                        "frame_id": frame_id,

                        "start_time": round(
                            start_time,
                            3
                        ),
                        "energy":beats_per_scene,

                        "end_time": round(
                            end_time,
                            3
                        ),

                        "duration": round(
                            duration,
                            3
                        ),

                        "motion": random.choice(
                            self.motions
                        ),

                        "transition": random.choice(
                            self.transitions
                        ),

                        "zoom": round(
                            random.uniform(
                                1.04,
                                1.12
                            ),
                            2
                        ),

                        "brightness": round(
                            random.uniform(
                                0.96,
                                1.05
                            ),
                            2
                        ),

                        "contrast": round(
                            random.uniform(
                                0.97,
                                1.08
                            ),
                            2
                        )

                    }

=======
                frames.append(
                    {
                        "frame_id": frame_id,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": duration
                    }
>>>>>>> origin
                )

                frame_id += 1

            ###################################################
<<<<<<< HEAD
            # Logging
            ###################################################

            log_info(

                f"{len(frames)} cinematic frames generated | "

                f"BPM={tempo:.2f} | "

                f"Scene={scene_duration:.1f}s | "

                f"Audio={total_duration:.2f}s"

=======

            log_info(
                f"{len(frames)} smart frames generated."
>>>>>>> origin
            )

            return frames

        except Exception as error:

            log_error(
<<<<<<< HEAD

                f"Frame Generation Failed : {error}"

=======
                f"Frame Generation Failed : {error}"
>>>>>>> origin
            )

            raise