

import random

from backend.app.utils.logger import (
    log_info,
    log_error
)


class PromptBuilder:
    """
    Build cinematic prompts for CLIP,
    Stable Diffusion and future AI models.
    """

    def __init__(self):

        log_info("PromptBuilder initialized.")

        # Mood Prompts
        self.mood_prompts = {

            "nature": [
                "peaceful nature",
                "lush green landscape",
                "beautiful natural scenery",
                "calm outdoor environment"
            ],

            "romantic": [
                "romantic atmosphere",
                "warm emotional scene",
                "love inspired landscape",
                "soft romantic lighting"
            ],

            "sad": [
                "lonely environment",
                "melancholic atmosphere",
                "rainy emotional scenery",
                "dramatic cinematic mood"
            ],

            "lofi": [
                "peaceful urban evening",
                "cozy aesthetic scene",
                "relaxing lo-fi environment",
                "calm evening street"
            ]
        }

        ####################################################
        # Category Prompts
        ####################################################

        self.category_prompts = {

            "forest": [
                "dense green forest",
                "beautiful jungle",
                "trees with sunlight",
                "misty forest path"
            ],

            "mountains": [
                "snow covered mountains",
                "cinematic mountain valley",
                "rocky mountain peaks",
                "high altitude landscape"
            ],

            "sunset": [
                "golden sunset",
                "orange evening sky",
                "beautiful sunset horizon",
                "warm golden hour"
            ],

            "nature": [
                "beautiful greenery",
                "fresh natural landscape",
                "green valley",
                "peaceful countryside"
            ]
        }

        ####################################################
        # Energy Prompts
        ####################################################

        self.energy_prompts = {

            "low": [
                "soft lighting",
                "slow cinematic camera",
                "peaceful atmosphere",
                "calm composition"
            ],

            "medium": [
                "natural lighting",
                "balanced composition",
                "realistic colors",
                "smooth camera movement"
            ],

            "high": [
                "dramatic lighting",
                "dynamic composition",
                "epic cinematic view",
                "high energy atmosphere"
            ]
        }

        ####################################################
        # Camera Styles
        ####################################################

        self.camera_styles = [

            "professional photography",
            "cinematic composition",
            "wide angle shot",
            "drone photography",
            "35mm photography",
            "ultra realistic composition"
        ]

        ####################################################
        # Quality Tags
        ####################################################

        self.quality_tags = [

            "photorealistic",
            "ultra detailed",
            "8k",
            "HDR",
            "sharp focus",
            "depth of field",
            "high quality"
        ]

    ####################################################
    # Build Prompt
    ####################################################

    def build_prompt(
        self,
        mood: str,
        category: str,
        energy: str
    ) -> str:

        try:

            mood_text = random.choice(
                self.mood_prompts.get(
                    mood,
                    ["beautiful environment"]
                )
            )

            category_text = random.choice(
                self.category_prompts.get(
                    category,
                    [category]
                )
            )

            energy_text = random.choice(
                self.energy_prompts.get(
                    energy,
                    ["natural lighting"]
                )
            )

            camera = random.choice(
                self.camera_styles
            )

            quality = ", ".join(
                random.sample(
                    self.quality_tags,
                    4
                )
            )

            prompt = (
                f"{category_text}, "
                f"{mood_text}, "
                f"{energy_text}, "
                f"{camera}, "
                f"{quality}"
            )

            return prompt

        except Exception as error:

            log_error(
                f"Prompt Builder Failed : {error}"
            )

            raise

    ####################################################
    # Build Scene Prompts
    ####################################################

    def build_scene_prompts(
        self,
        scenes: list
    ) -> dict:

        """
        Generate prompts for every scene.

        Parameters
        ----------
        scenes : list

        Returns
        -------
        dict
        """

        prompts = {}

        try:

            for scene in scenes:

                scene_id = scene["scene_id"]

                prompts[scene_id] = self.build_prompt(

                    mood=scene["mood"],

                    category=scene["category"],

                    energy=scene["energy"]

                )

            log_info(
                f"{len(prompts)} scene prompts generated."
            )

            return prompts

        except Exception as error:

            log_error(
                f"Scene Prompt Generation Failed : {error}"
            )

            raise