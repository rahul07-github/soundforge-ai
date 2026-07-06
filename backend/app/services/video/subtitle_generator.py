"""
Project : SoundForge AI

Module : Subtitle Generator

Description:
Generate subtitle (.srt) file from lyrics.
"""

from pathlib import Path

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.file_manager import create_directory

class SubtitleGenerator:
    """
    Generate subtitle file from lyrics.
    """

    def __init__(self):
        log_info("SubtitleGenerator initialized.")

    def generate_subtitle(
        self,
        lyrics_path: str,
        output_path: str
    ) -> str:

        """
        Generate SRT subtitle.

        Parameters
        ----------
        lyrics_path : str

        output_path : str

        Returns
        -------
        str
        """

        try:

            log_info("Generating subtitles...")

            with open(
                lyrics_path,
                "r",
                encoding="utf-8"
            ) as file:

                lyrics = file.readlines()

            subtitle_file = Path(output_path)
            create_directory(subtitle_file.parent)

            with open(
                subtitle_file,
                "w",
                encoding="utf-8"
            ) as file:

                start = 0

                for index, line in enumerate(lyrics):

                    end = start + 4

                    file.write(
                        f"{index+1}\n"
                    )

                    file.write(
                        f"00:00:{start:02},000 --> 00:00:{end:02},000\n"
                    )

                    file.write(
                        line.strip() + "\n\n"
                    )

                    start = end

            log_info(
                f"Subtitle saved : {subtitle_file}"
            )

            return str(subtitle_file)

        except Exception as error:

            log_error(
                f"Subtitle Generation Failed : {error}"
            )

            raise