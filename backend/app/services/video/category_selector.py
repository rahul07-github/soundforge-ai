## Ye module mood ke hisaab se decide karega ki kaun se dataset folders use honge.

"""
Project : SoundForge AI

Module : Category Selector

Description:
Select image dataset categories according
to the detected song mood.
"""

from backend.app.utils.logger import (log_info,log_error)

class CategorySelector:
    """
    Select dataset categories based on mood.
    """

    def __init__(self):

        log_info("CategorySelector initialized.")

    
        # Mood → Dataset Categories
        

        self.category_map = {

            "sad": [
                "sad",
                "lofi",
                "sunset"
            ],

            "romantic": [
                "romantic",
                "sunset",
                "nature"
            ],

            "lofi": [
                "lofi",
                "nature",
                "sunset"
            ],

            "nature": [
                "nature",
                "forest",
                "mountains",
                "sunset"
            ],

            "travel": [
                "mountains",
                "forest",
                "nature"
            ],

            "mountains": [
                "mountains",
                "nature",
                "forest"
            ],

            "forest": [
                "forest",
                "nature"
            ],

            "sunset": [
                "sunset",
                "nature"
            ]
        }

    def select_categories(
        self,
        mood: str
    ) -> list:
        """
        Select dataset categories according to mood.

        Parameters
        ----------
        mood : str

        Returns
        -------
        list
        """

        try:

            mood = mood.lower()

            ####################################################
            # Known Mood
            ####################################################

            if mood in self.category_map:

                categories = self.category_map[mood]

            ####################################################
            # Unknown Mood
            ####################################################

            else:

                categories = [
                    "nature"
                ]

            log_info(
                f"Selected Categories : {categories}"
            )

            return categories

        except Exception as error:

            log_error(
                f"Category Selection Failed : {error}"
            )

            raise