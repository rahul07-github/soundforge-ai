##   ==== 

import cv2

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.constants import VIDEO_WIDTH, VIDEO_HEIGHT


class ImageProcessor:
    """
    Image processing for AI Video Generation.
    """

    def __init__(self):
        log_info("ImageProcessor initialized.")

    def process_images(
        self,
        frames: list,
        cover_path: str
    ) -> list:

        """
        Process cover image for each frame.
        """

        try:
            log_info(
                f"Loading cover image : {cover_path}"
            )
            image = cv2.imread(cover_path)
            if image is None:
                raise FileNotFoundError(
                    f"Image not found : {cover_path}"
                )

            ###################################################
            # Resize
            ###################################################

            image = cv2.resize(
                image,
                (
                    VIDEO_WIDTH,
                    VIDEO_HEIGHT
                )
            )

            ###################################################
            # Convert BGR → RGB
            ###################################################

            image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            ###################################################
            # Prepare Frame Data
            ###################################################

            processed_frames = []
            for frame in frames:
                processed_frames.append(
                    {
                        "frame_id": frame["frame_id"],

                        "image": image.copy(),

                        "start_time": frame["start_time"],

                        "end_time": frame["end_time"],

                        "duration": frame["duration"]
                    }
                )
            log_info(
                f"{len(processed_frames)} images processed."
            )
            return processed_frames
        except Exception as error:
            log_error(
                f"Image Processing Failed : {error}"
            )
            raise