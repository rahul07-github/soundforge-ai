"""
Project : SoundForge AI

Module : Image Mixer

Description:
Create a smart cinematic image sequence.
"""

import random

from backend.app.utils.logger import (
    log_info,
    log_error
)


class ImageMixer:
    """
    Mix images intelligently instead of randomly.
    """

    def __init__(self):

        log_info("ImageMixer initialized.")

        ####################################################
        # Mood Priority
        ####################################################

        self.category_weights = {

            "romantic": 0.60,
            "sunset": 0.25,
            "nature": 0.15,

            "sad": 0.60,
            "lofi": 0.25,

            "forest": 0.30,
            "mountains": 0.20

        }

    ####################################################
    # Build Weighted Pool
    ####################################################

    def build_pool(
        self,
        datasets: dict
    ) -> list:

        pool = []

        for category, images in datasets.items():

            shuffled = images.copy()

            random.shuffle(shuffled)

            weight = self.category_weights.get(
                category,
                0.20
            )

            repeat = max(
                1,
                round(weight * 10)
            )

            for image in shuffled:

                pool.extend(
                    [image] * repeat
                )

            log_info(
                f"{category} -> {len(shuffled)} images"
            )

        random.shuffle(pool)

        return pool

    ####################################################
    # Mix Images
    ####################################################

    def mix_images(
        self,
        datasets: dict,
        frame_count: int
    ) -> list:

        try:

            image_pool = self.build_pool(datasets)

            if len(image_pool) == 0:

                raise Exception(
                    "Dataset is empty."
                )

            mixed_images = []

            used = set()

            last_image = None

            ####################################################
            # Generate Image Timeline
            ####################################################

            while len(mixed_images) < frame_count:

                random.shuffle(image_pool)

                selected = None

                for image in image_pool:

                    if image != last_image and image not in used:

                        selected = image
                        break

                ################################################
                # All images already used
                ################################################

                if selected is None:

                    used.clear()

                    continue

                mixed_images.append(selected)

                used.add(selected)

                last_image = selected

            ####################################################
            # Final Log
            ####################################################

            log_info(
                f"Frames Needed : {frame_count}"
            )

            log_info(
                f"Images Mixed  : {len(mixed_images)}"
            )

            return mixed_images

        except Exception as error:

            log_error(
                f"Image Mixing Failed : {error}"
            )

            raise