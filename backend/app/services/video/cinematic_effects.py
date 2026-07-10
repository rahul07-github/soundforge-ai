"""
Project : SoundForge AI

Module : Cinematic Effects

Description:
Apply cinematic camera movement effects.
"""

import random

from moviepy.editor import ImageClip

from backend.app.utils.logger import (
    log_info,
    log_error
)


class CinematicEffects:
    """
    Apply cinematic movement to image clips.
    """

    def __init__(self):

        log_info("CinematicEffects initialized.")

        self.effects = [

            "zoom_in",

            "zoom_out",

            "pan_left",

            "pan_right",

            "pan_up",

            "pan_down"

        ]

    def apply_effect(
        self,
        image,
        duration: float
    ) -> ImageClip:
        """
        Create cinematic clip.

        Parameters
        ----------
        image : ndarray

        duration : float

        Returns
        -------
        ImageClip
        """

        try:

            effect = random.choice(
                self.effects
            )

            clip = (
                ImageClip(image)
                .set_duration(duration)
            )

            
            # Zoom In
            

            if effect == "zoom_in":

                clip = clip.resize(
                    lambda t:
                    1 + 0.12 * (t / duration)
                )

            
            # Zoom Out
            

            elif effect == "zoom_out":

                clip = clip.resize(
                    lambda t:
                    1.12 - 0.12 * (t / duration)
                )

            
            # Pan Left
            

            elif effect == "pan_left":

                clip = clip.set_position(

                    lambda t: (

                        -40 * (t / duration),

                        "center"

                    )

                )

            
            # Pan Right
            

            elif effect == "pan_right":

                clip = clip.set_position(

                    lambda t: (

                        40 * (t / duration),

                        "center"

                    )

                )

            
            # Pan Up
            

            elif effect == "pan_up":
                clip = clip.set_position(
                    lambda t: (
                        "center",
                        -30 * (t / duration)

                    )
                )  
            # Pan Down
            

            elif effect == "pan_down":

                clip = clip.set_position(

                    lambda t: (

                        "center",

                        30 * (t / duration)

                    )

                )

            log_info(
                f"Cinematic Effect : {effect}"
            )

            return clip

        except Exception as error:

            log_error(
                f"Cinematic Effect Failed : {error}"
            )

            raise