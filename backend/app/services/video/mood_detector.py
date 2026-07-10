"""
Project : SoundForge AI

Module : Mood Detector

Description:
Detect song mood from metadata.
"""

from backend.app.utils.logger import (
    log_info,
    log_error
)


class MoodDetector:
    """
    Detect song mood using metadata.
    """

    def __init__(self):
        log_info("MoodDetector initialized.")

    def detect_mood(
        self,
        metadata: dict
    ) -> str:
        """
        Detect mood from metadata.

        Parameters
        ----------
        metadata : dict

        Returns
        -------
        str
            Song mood.
        """

        try:

            ##################################################
            # Highest Priority
            ##################################################

            if metadata.get("mood"):

                mood = metadata["mood"].lower()

            ##################################################
            # Second Priority
            ##################################################

            elif metadata.get("emotion"):

                mood = metadata["emotion"].lower()

            ##################################################
            # Third Priority
            ##################################################

            elif metadata.get("genre"):

                mood = metadata["genre"].lower()

            ##################################################
            # Default
            ##################################################

            else:
                mood = "nature"

            log_info(
                f"Detected Mood : {mood}"
            )

            return mood

        except Exception as error:
            log_error(
                f"Mood Detection Failed : {error}"
            )
            raise