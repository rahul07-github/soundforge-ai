import random

from backend.app.utils.logger import (
    log_info,
    log_error
)
from backend.app.services.video.image_ranker import ImageRanker


class ImageMixer:
    """
    Mix images intelligently instead of randomly, using
    CLIP-based ranking and mood-weighted repetition.
    """

    def __init__(self):

        log_info("ImageMixer initialized.")

        self.image_ranker = ImageRanker()

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
    # Build Weighted, CLIP-Ranked Pool
    ####################################################

    def build_pool(
        self,
        datasets: dict,
        prompts: dict
    ) -> list:
        """
        Rank each category's images using CLIP, then build
        a weighted pool where higher-priority categories
        appear more often.
        """

        pool = []

        for category, images in datasets.items():

            prompt = prompts.get(category, category)

            ranked = self.image_ranker.rank_images(
                images,
                prompt
            )

            ranked_paths = [
                item["image_path"]
                for item in ranked
            ]

            weight = self.category_weights.get(
                category,
                0.20
            )

            repeat = max(
                1,
                round(weight * 10)
            )

            for image in ranked_paths:
                pool.extend([image] * repeat)

            log_info(
                f"{category} -> {len(ranked_paths)} images "
                f"(repeat factor: {repeat})"
            )

        random.shuffle(pool)

        return pool

    ####################################################
    # Mix Images (now correctly reuses build_pool)
    ####################################################

    def mix_images(
        self,
        datasets: dict,
        frame_count: int,
        prompts: dict
    ) -> list:
        """
        Generate a final ordered image timeline for the video,
        avoiding immediate repeats, using the CLIP-ranked,
        weighted pool from build_pool().

        Parameters
        ----------
        datasets : dict
            {category: [image_paths]}

        frame_count : int
            Total number of frames needed.

        prompts : dict
            {category: descriptive text prompt for CLIP ranking}
        """

        try:

            image_pool = self.build_pool(datasets, prompts)

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
                # All images already used -> reset used-tracker
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

            log_info(f"Frames Needed : {frame_count}")
            log_info(f"Images Mixed  : {len(mixed_images)}")

            return mixed_images

        except Exception as error:

            log_error(f"Image Mixing Failed : {error}")

            raise