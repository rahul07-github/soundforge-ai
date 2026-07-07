# In this we customize clip  songs 

import subprocess
from pathlib import Path

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.constants import TEMP_FOLDER
from backend.app.utils.file_manager import create_directory


class AudioTrimmer:
    """
    Trim a portion of the song.
    """

    def __init__(self):
        log_info("AudioTrimmer initialized.")

    def trim_audio(
        self,
        song_path: str,
        start_time: int = 30,
        duration: int = 20
    ) -> str:

        try:

            log_info(
                f"Trimming audio ({start_time}s - {start_time + duration}s)"
            )

            create_directory(TEMP_FOLDER)

            filename = build_output_filename(
                "clip",
                "mp3"
            )

            output_path = str(
                Path(TEMP_FOLDER) / filename
            )

            command = [
                "ffmpeg",
                "-y",

                "-ss",
                str(start_time),
                "-i",
                song_path,

                "-t",
                str(duration),
                "-acodec",
                "libmp3lame",

                "-q:a",
                "2",
                output_path
            ]

            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            if not Path(output_path).exists():
                raise FileNotFoundError(
                    f"Trimmed audio not created: {output_path}"
         )

            if Path(output_path).stat().st_size == 0:
                raise Exception(
                    "Trimmed audio file is empty."
                )

            log_info(
                f"Audio Clip Saved : {output_path}"
            )

            return output_path

        except subprocess.CalledProcessError as error:

            log_error(error.stderr)

            raise

        except Exception as error:

            log_error(str(error))

            raise