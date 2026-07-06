
import ffmpeg
from pathlib import Path

from backend.app.utils.file_manager import create_directory
from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.constants import TEMP_FOLDER


class AudioMerger:
    """
    Merge silent video and audio.
    """

    def __init__(self):

        log_info("AudioMerger initialized.")

    def merge_audio(
        self,
        silent_video: str,
        song_path: str
    ) -> str:

        """
        Merge video with audio.

        Parameters
        ----------
        silent_video : str

        song_path : str

        Returns
        -------
        str
        """

        try:

            log_info("Merging audio with video.")

            create_directory(TEMP_FOLDER)
            filename = build_output_filename(
                "merged_video",
                "mp4"
            )
            output_path = Path(TEMP_FOLDER) / filename

            (
                ffmpeg.output(
                    ffmpeg.input(silent_video),
                    ffmpeg.input(song_path),
                    str(output_path),
                    vcodec="copy",
                    acodec="aac",
                    shortest=None
                )
                .overwrite_output()
                .run(quiet=True)
            )

            log_info(
                f"Audio merged successfully : {output_path}"
            )

            return str(output_path)

        except Exception as error:

            log_error(
                f"Audio Merge Failed : {error}"
            ) 
            raise
