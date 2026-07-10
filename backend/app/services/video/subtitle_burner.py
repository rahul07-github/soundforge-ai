import subprocess
import shutil
from pathlib import Path

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.file_manager import create_directory
from backend.app.utils.constants import TEMP_FOLDER



class SubtitleBurner:
    """Burn subtitles permanently into the video."""

    def __init__(self):
        log_info("SubtitleBurner initialized.")

    def burn_subtitles(
        self,
        video_path: str,
        subtitle_path: str
    ) -> str:

        try:

            log_info("Burning subtitles into video...")

            create_directory(TEMP_FOLDER)

            filename = build_output_filename(
                "subtitle_video",
                "mp4"
            )

            output_path = str(
                Path(TEMP_FOLDER) / filename
            )

            temp_dir = Path(TEMP_FOLDER)

            input_video = temp_dir / "input.mp4"

            input_subtitle = temp_dir / "subtitle.srt"

            shutil.copy2(video_path, input_video)

            shutil.copy2(subtitle_path, input_subtitle)



#            subtitle_filter = (Path(subtitle_path).resolve().as_posix())

#            subtitle_filter=subtitle_filter.replace(":", "\\:")

            command = [
                "ffmpeg",
                "-y",
                "-i",
                "input.mp4",
                "-vf",
                f"subtitles=subtitle.srt",
                "-c:a",
                "copy",
                Path(output_path).name
            ]

            subprocess.run(
                command,
                cwd=temp_dir,
                check=True,
                capture_output=True,
                text=True
            )

            log_info(
                f"Subtitle Burn Completed : {output_path}"
            )

            return output_path

        except subprocess.CalledProcessError as error:

            log_error(error.stderr)

            raise

        except Exception as error:

            log_error(str(error))

            raise