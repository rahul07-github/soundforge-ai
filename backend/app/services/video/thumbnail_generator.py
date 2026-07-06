# Thumbnail Generator

from pathlib import Path

import cv2

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.file_manager import create_directory
from backend.app.utils.constants import THUMBNAIL_FOLDER


class ThumbnailGenerator:
    """
    Generate thumbnail from final video.
    """

    def __init__(self):
        log_info("ThumbnailGenerator initialized.")

    def generate_thumbnail(self, video_path: str) -> str:
        """
        Generate thumbnail from video.

        Parameters
        ----------
        video_path : str

        Returns
        -------
        str
            Thumbnail path.
        """

        try:

            log_info("Generating thumbnail...")

            create_directory(THUMBNAIL_FOLDER)

            filename = build_output_filename(
                "thumbnail",
                "png"
            )

            thumbnail_path = Path(THUMBNAIL_FOLDER) / filename

            capture = cv2.VideoCapture(str(video_path))

            success, frame = capture.read()

            if not success:
                raise Exception(
                    "Unable to read video."
                )

            cv2.imwrite(
                str(thumbnail_path),
                frame
            )

            capture.release()

            log_info(
                f"Thumbnail saved : {thumbnail_path}"
            )

            return str(thumbnail_path)

        except Exception as error:

            log_error(
                f"Thumbnail Generation Failed : {error}"
            )

            raise