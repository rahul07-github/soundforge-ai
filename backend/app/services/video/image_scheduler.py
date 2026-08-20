#

import random

from backend.app.utils.logger import (
    log_info,
    log_error
)


class ImageScheduler:
    """
    Schedule images for every frame.
    """

    def __init__(self):

        log_info("ImageScheduler initialized.")

        self.transitions = [
            "crossfade",
            "fade",
            "zoom"
        ]

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
    # Schedule Images
    def schedule_images(
        self,
        frames: list,
        scenes: list,
        mixed_images: list
    ) -> list:

        try:

            if len(mixed_images) == 0:

                raise Exception(
                    "No images available."
                )

            image_pool = mixed_images.copy()

            random.shuffle(image_pool)

            scheduled = []

            last_image = None
            last_motion = None

            total_frames = len(frames)

            for index, frame in enumerate(frames):

                # Reload Pool
                if len(image_pool) == 0:

                    image_pool = mixed_images.copy()

                    random.shuffle(image_pool)

                
                # Pick Image  

                image = image_pool.pop(0)

                if image == last_image and len(image_pool) > 0:

                    image_pool.append(image)

                    image = image_pool.pop(0)

                
                # Song Progress

                scene=scenes[
                    min(index, len(scenes) - 1)
                ]
                energy=scene["energy"]
                category=scene["category"]

            
                # Energy Curve

                # if progress < 0.20:
                #     energy = "low"

                # elif progress < 0.45:
                #     energy = "medium"

                # elif progress < 0.75:
                #     energy = "high"

                # else:
                #     energy = "medium"

                ################################################
                # Motion Selection
                ################################################

                if energy < 0.40:
                    candidates = [
                        "zoom_in",
                        "pan_left",
                        "pan_right"
                    ]

                elif energy < 0.75:
                    candidates = [
                        "zoom_out",
                        "pan_up",
                        "pan_down",
                        "diagonal_left"
                    ]
                else:
                    candidates = [
                        "diagonal_left",
                        "diagonal_right",
                        "zoom_in",
                        "zoom_out"
                    ]

                motion = random.choice(candidates)

                while (
                    motion == last_motion
                    and len(candidates) > 1
                ):
                    motion = random.choice(candidates)

                # Transition
                

                if energy == "low":
                    transition = "crossfade"

                elif energy == "medium":
                    transition = random.choice(
                        [
                            "crossfade",
                            "fade"
                        ]
                    )
                else:
                    transition = random.choice(
                        self.transitions
                    )

                
                # Store Scene

                scheduled.append(
                    {
                        "scene_id":scene["scene_id"],
                        "category":category,
                        "scene_duration":scene["duration"],

                        "frame": frame,

                        "image_path": image,

                        "motion": motion,

                        "transition": transition,

                        "energy": energy,

                        "zoom": round(
                            random.uniform(
                                1.05,
                                1.10
                            ),
                            2
                        ),

                        "brightness": round(
                            random.uniform(
                                0.98,
                                1.03
                            ),
                            2
                        ),

                        "contrast": round(
                            random.uniform(
                                1.00,
                                1.08
                            ),
                            2
                        )
                    }
                )

                last_image = image
                last_motion = motion


            # Logs

            log_info(
                f"Frames Scheduled : {len(scheduled)}"
            )
            log_info(
                f"Scenes Available: {len(scenes)}"
            )

            log_info(
                f"Images Used : {len(set(item['image_path'] for item in scheduled))}"
            )

            return scheduled

        except Exception as error:

            log_error(
                f"Image Scheduling Failed : {error}"
            )

            raise