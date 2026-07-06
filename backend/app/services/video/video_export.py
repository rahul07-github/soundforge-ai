## Video Exporter 

import shutil
from pathlib import Path

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.file_manager import create_directory
from backend.app.utils.constants import VIDEO_FOLDER


class VideoExporter:
    """
    Export final video to storage/generated/videos/
    """

    def __init__(self):
        log_info("VideoExporter initialized.")

    def export_video(self, merged_video_path: str) -> str:
        """
        Export merged video.

        Parameters
        ----------
        merged_video_path : str

        Returns
        -------
        str
            Final exported video path.
        """

        try:

            log_info("Exporting final video...")

            # Ensure destination folder exists
            create_directory(VIDEO_FOLDER)

            # Generate unique filename
            filename = build_output_filename(
                prefix="video",
                extension="mp4"
            )

            destination = Path(VIDEO_FOLDER) / filename

            # Copy merged video to final destination
            shutil.copy2(
                merged_video_path,
                destination
            )

            log_info(
                f"Video exported successfully : {destination}"
            )

            return str(destination)

        except Exception as error:

            log_error(
                f"Video Export Failed : {error}"
            )

            raise