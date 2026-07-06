"""
Project : SoundForge AI

Module : Video Generator

Description:
Creates a silent video from processed frames.
"""

from moviepy.editor import ImageSequenceClip

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.constants import TEMP_FOLDER
from backend.app.utils.file_manager import create_directory

class VideoGenerator:
    """
    Generate silent video from processed frames.
    """

    def __init__(self):
        log_info("VideoGenerator initialized.")

    def generate_video(self, processed_frames: list) -> str:

        """
        Generate temporary silent video.
        Parameters
        ----------
        processed_frames : listReturns
        -------
        str
            Temporary video path.
        """
        try:
            log_info("Generating silent video.")
            images = []
            fps = 30

            ##################################################
            # Collect Images
            ##################################################

            for frame in processed_frames:
                image = frame["image"]
                duration = frame["duration"]
                repeat = max(1, int(duration * fps))
                for _ in range(repeat):
                    images.append(image)

            ##################################################
            # Create Video
            ##################################################

            clip = ImageSequenceClip(
                images,
                fps=fps
            )

            ##################################################
            # Output Path
            ##################################################

            create_directory(TEMP_FOLDER)

            filename = build_output_filename(
                "temp_video",
                "mp4"
            )

            output_path = TEMP_FOLDER / filename

            ##################################################
            # Save
            ##################################################

            clip.write_videofile(
                str(output_path),
                codec="libx264",
                audio=False,
                logger=None
            )
            log_info(
                f"Silent video created : {output_path}"
            )
            return str(output_path)

        except Exception as error:
            log_error(

                f"Video Generation Failed : {error}"
            )
            raise