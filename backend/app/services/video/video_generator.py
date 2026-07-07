"""
Project : SoundForge AI

Module : Video Generator

Description:
Creates a silent cinematic video from processed frames.
"""

import random

from moviepy.editor import (
    ImageClip,
    CompositeVideoClip
)

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.helper import build_output_filename
from backend.app.utils.constants import (
    TEMP_FOLDER,
    VIDEO_WIDTH,
    VIDEO_HEIGHT
)
from backend.app.utils.file_manager import create_directory


class VideoGenerator:
    """
    Generate silent cinematic video.
    """

    def __init__(self):
        log_info("VideoGenerator initialized.")

    def generate_video(self, processed_frames: list) -> str:

        try:

            log_info("Generating silent video.")

            fps = 30
            transition = 0.40

            timeline = 0
            clips = []

            camera_effects = [
                "zoom_in",
                "zoom_out",
                "pan_left",
                "pan_right",
                "pan_up",
                "pan_down"
            ]

            ##################################################
            # Create Animated Clips
            ##################################################

            for frame in processed_frames:

                image = frame["image"]

                duration = max(
                    frame["duration"],
                    0.30
                )

                effect = random.choice(
                    camera_effects
                )

                clip = (
                    ImageClip(image)
                    .set_duration(duration)
                    .resize(
                        (
                            VIDEO_WIDTH,
                            VIDEO_HEIGHT
                        )
                    )
                )

                ##################################################
                # Camera Motion
                ##################################################

                if effect == "zoom_in":

                    clip = clip.resize(
                        lambda t:
                        1 + 0.12 * (t / duration)
                    )

                elif effect == "zoom_out":

                    clip = clip.resize(
                        lambda t:
                        1.12 - 0.12 * (t / duration)
                    )

                elif effect == "pan_left":

                    clip = (
                        clip
                        .resize(1.08)
                        .set_position(
                            lambda t: (
                                -120 * t / duration,
                                "center"
                            )
                        )
                    )

                elif effect == "pan_right":

                    clip = (
                        clip
                        .resize(1.08)
                        .set_position(
                            lambda t: (
                                120 * t / duration,
                                "center"
                            )
                        )
                    )

                elif effect == "pan_up":

                    clip = (
                        clip
                        .resize(1.08)
                        .set_position(
                            lambda t: (
                                "center",
                                -80 * t / duration
                            )
                        )
                    )

                elif effect == "pan_down":

                    clip = (
                        clip
                        .resize(1.08)
                        .set_position(
                            lambda t: (
                                "center",
                                80 * t / duration
                            )
                        )
                    )

                ##################################################
                # Timeline
                ##################################################

                clip = (
                    clip
                    .set_start(timeline)
                    .crossfadein(transition)
                )

                timeline += duration - transition

                clips.append(clip)

            ##################################################
            # Composite Video
            ##################################################

            final_clip = CompositeVideoClip(
                clips,
                size=(
                    VIDEO_WIDTH,
                    VIDEO_HEIGHT
                )
            )

            final_clip = final_clip.set_duration(
                timeline + duration
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
            # Export
            ##################################################

            final_clip.write_videofile(
                str(output_path),
                codec="libx264",
                fps=fps,
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