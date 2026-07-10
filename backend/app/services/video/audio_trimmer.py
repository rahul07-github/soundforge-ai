<<<<<<< HEAD
"""
Project : SoundForge AI

Module : Audio Trimmer

Description:
Trim a suitable portion of the song automatically.
"""
=======
# In this we customize clip  songs 
>>>>>>> origin

import subprocess
from pathlib import Path

<<<<<<< HEAD
from pydub import AudioSegment

ffmpeg = r"D:\FFmpeg\bin\ffmpeg.exe"
ffprobe = r"D:\FFmpeg\bin\ffprobe.exe"

AudioSegment.converter = ffmpeg
AudioSegment.ffprobe = ffprobe

=======
>>>>>>> origin
from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.constants import TEMP_FOLDER
from backend.app.utils.file_manager import create_directory


class AudioTrimmer:
    """
<<<<<<< HEAD
    Trim a suitable clip from any song.
=======
    Trim a portion of the song.
>>>>>>> origin
    """

    def __init__(self):
        log_info("AudioTrimmer initialized.")

<<<<<<< HEAD
    def trim_audio(self, song_path: str, start_time: int = None, duration: int = None) -> str:

        try:

            # ------------------------------------------------
            # Check input file
            # ------------------------------------------------

            song = Path(song_path)

            if not song.exists():
                raise FileNotFoundError(
                    f"Input song not found: {song_path}"
                )

            print("=" * 60)
            print("INPUT SONG :", song_path)
            print("EXISTS     :", song.exists())
            print("SIZE       :", song.stat().st_size, "bytes")
            print("=" * 60)

            # ------------------------------------------------
            # Read song duration
            # ------------------------------------------------

            audio = AudioSegment.from_file(song_path)

            total_duration = len(audio) / 1000

            print(f"Song Duration : {total_duration:.2f} sec")

            # ------------------------------------------------
            # Decide clip automatically
            # ------------------------------------------------
            if start_time is None or duration is None:

                if total_duration <= 20:

                    start_time = 0
                    duration = int(total_duration)

                elif total_duration <= 60:

                    duration = 20
                    start_time = int((total_duration - duration) / 2)

                elif total_duration <= 180:

                    duration = 30
                    start_time = int((total_duration - duration) / 2)

                else:

                    duration = 45
                    start_time = int((total_duration - duration) / 2)

=======
    def trim_audio(
        self,
        song_path: str,
        start_time: int = 30,
        duration: int = 20
    ) -> str:

        try:

>>>>>>> origin
            log_info(
                f"Trimming audio ({start_time}s - {start_time + duration}s)"
            )

<<<<<<< HEAD
            # ------------------------------------------------
            # Output path
            # ------------------------------------------------

=======
>>>>>>> origin
            create_directory(TEMP_FOLDER)

            filename = build_output_filename(
                "clip",
                "mp3"
            )

            output_path = str(
                Path(TEMP_FOLDER) / filename
            )

<<<<<<< HEAD
            # ------------------------------------------------
            # FFmpeg
            # ------------------------------------------------

            command = [
                ffmpeg,
                "-y",
=======
            command = [
                "ffmpeg",
                "-y",

>>>>>>> origin
                "-ss",
                str(start_time),
                "-i",
                song_path,
<<<<<<< HEAD
=======

>>>>>>> origin
                "-t",
                str(duration),
                "-acodec",
                "libmp3lame",
<<<<<<< HEAD
=======

>>>>>>> origin
                "-q:a",
                "2",
                output_path
            ]

<<<<<<< HEAD
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            print("=" * 60)
            print("FFMPEG RETURN CODE :", result.returncode)
            print(result.stderr)
            print("=" * 60)

            result.check_returncode()

            # ------------------------------------------------
            # Validate output
            # ------------------------------------------------

            output = Path(output_path)

            if not output.exists():
                raise FileNotFoundError(
                    f"Trimmed audio not created: {output_path}"
                )

            size = output.stat().st_size

            print("OUTPUT SIZE :", size, "bytes")

            if size < 5000:
                raise Exception(
                    "Trimmed audio is too small or invalid."
=======
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
>>>>>>> origin
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