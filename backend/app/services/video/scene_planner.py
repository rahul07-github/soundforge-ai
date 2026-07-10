"""
Project : SoundForge AI

Module : Scene Planner

Description:
Create cinematic scenes from detected beats.
"""

import math

from backend.app.utils.logger import (
    log_info,
    log_error
)


class ScenePlanner:
    """
    Create scene timeline using beat information.
    """

    def __init__(self):

        log_info("ScenePlanner initialized.")

    def estimate_energy(
        self,
        tempo: float
    ) -> float:
        """
        Estimate song energy from BPM.
        """

        if tempo < 80:
            return 0.30

        elif tempo < 110:
            return 0.45

        elif tempo < 140:
            return 0.65

        elif tempo < 170:
            return 0.85

        return 1.00

    def create_scenes(
        self,
        beat_data: dict,
        categories: list
    ) -> list:
        """
        Create cinematic scenes.

        Parameters
        ----------
        beat_data : dict

        categories : list

        Returns
        -------
        list
        """

        try:

            beat_times = beat_data["beat_times"]
            tempo = beat_data["tempo"]

            if len(beat_times) < 2:

                raise Exception(
                    "Not enough beats detected."
                )

            ####################################################
            # Configuration
            ####################################################

            TARGET_SCENE_DURATION = 5.0

            ####################################################
            # Audio Duration
            ####################################################

            total_duration = beat_times[-1]

            total_scenes = max(
                1,
                math.ceil(
                    total_duration /
                    TARGET_SCENE_DURATION
                )
            )

            beats_per_scene = max(
                1,
                math.ceil(
                    len(beat_times) /
                    total_scenes
                )
            )

            ####################################################
            # Energy
            ####################################################

            energy = self.estimate_energy(
                tempo
            )

            ####################################################
            # Scene Creation
            ####################################################

            scenes = []

            scene_id = 1

            category_index = 0

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

                category = categories[
                    category_index %
                    len(categories)
                ]

                scenes.append(

                    {

                        "scene_id": scene_id,

                        "start_time": round(
                            start_time,
                            2
                        ),

                        "end_time": round(
                            end_time,
                            2
                        ),

                        "duration": round(
                            duration,
                            2
                        ),

                        "category": category,

                        "energy": energy

                    }

                )

                scene_id += 1

                category_index += 1
                
            log_info(
                f"{len(scenes)} scenes created."
            )
            return scenes
        except Exception as error:
            log_error(
                f"Scene Planning Failed : {error}"
            )
            raise