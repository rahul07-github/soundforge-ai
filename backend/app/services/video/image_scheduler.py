"""
Project : SoundForge AI

Module : Image Scheduler

Description:
Create a cinematic image schedule for every frame.
"""

import random

from backend.app.utils.logger import (
    log_info,
    log_error
)


class ImageScheduler:
    """
    Smart scheduler for cinematic videos.
    """

    def __init__(self):

        log_info("ImageScheduler initialized.")

        self.transitions = [
            "crossfade",
            "crossfade",
            "crossfade",
            "fade",
            "soft",
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

    def schedule_images(
        self,
        frames: list,
        mixed_images: list
    ) -> list:

        try:

            if not mixed_images:
                raise Exception("No images available.")

            image_pool = mixed_images.copy()
            random.shuffle(image_pool)

            scheduled = []

            used_images = []

            last_image = None
            last_motion = None

            total_frames = len(frames)

            for index, frame in enumerate(frames):

                ################################################
                # Reload image pool
                ################################################

                if not image_pool:

                    image_pool = [
                        img
                        for img in mixed_images
                        if img not in used_images[-12:]
                    ]

                    if not image_pool:
                        image_pool = mixed_images.copy()

                    random.shuffle(image_pool)

                ################################################
                # Image Selection
                ################################################

                image = image_pool.pop(0)

                if image == last_image and image_pool:

                    image_pool.append(image)
                    image = image_pool.pop(0)

                ################################################
                # Song Progress
                ################################################

                progress = index / max(1, total_frames)

                energy=frame["energy"]

                ################################################
                # Motion Selection
                ################################################

                ################################################
                # Motion Based On Beat Energy
                ################################################

                if energy <= 2:

                    candidates = [
                        "zoom_in",
                        "zoom_out"
                    ]

                elif energy <= 5:

                    candidates = [
                        "pan_left",
                        "pan_right",
                        "pan_up",
                        "pan_down"
                    ]

                else:

                    candidates = [
                        "diagonal_left",
                        "diagonal_right",
                        "zoom_in",
                        "zoom_out"
                    ]

                motion = random.choice(candidates)

                while motion == last_motion and len(candidates) > 1:

                    motion = random.choice(candidates)

                motion = random.choice(candidates)

                while motion == last_motion and len(candidates) > 1:
                    motion = random.choice(candidates)

                ################################################
                # Transition
                ################################################

                if energy <= 2:

                    transition = "soft"

                elif energy <= 5:

                    transition = "crossfade"

                else:

                    transition = random.choice([
                        "zoom",
                        "crossfade"
                    ])

                ################################################
                # Scene
                ################################################

                scheduled.append({

                    "scene_id": index + 1,

                    "frame": frame,

                    "image_path": image,

                    "motion": motion,

                    "transition": transition,

                    "zoom": (
                        1.04
                        if energy <= 2
                        else 1.08
                        if energy <= 5
                        else 1.12
                    ),

                    "brightness": (
                        0.98
                        if energy <= 2
                        else 1.00
                        if energy <= 5
                        else 1.03
                    ),

                    "brightness": (
                        0.98
                        if energy <= 2
                        else 1.00
                        if energy <= 5
                        else 1.03
                    ),

                })

                last_image = image
                last_motion = motion
                used_images.append(image)

            log_info(
                f"Frames Scheduled : {len(scheduled)}"
            )

            log_info(
                f"Unique Images Used : {len(set(used_images))}"
            )

            return scheduled

        except Exception as error:

            log_error(
                f"Image Scheduling Failed : {error}"
            )

            raise