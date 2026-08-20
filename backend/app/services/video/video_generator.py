"""
Project : SoundForge AI

Module : Video Generator

Description:
Generate smooth cinematic silent videos using MoviePy.
"""

import random
import math

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
    Professional Video Generator
    """

    def __init__(self):

        log_info("VideoGenerator initialized.")

        ####################################################
        # Configuration
        ####################################################

        self.fps = 30
        self.transition_duration = 0.8
        self.max_zoom = 1.08
        self.pan_distance_x = 120
        self.pan_distance_y = 70
        self.rotation_angle = 0.5

        self.motion_types = [
            "zoom_in", "zoom_out", "pan_left", "pan_right",
            "pan_up", "pan_down", "diagonal_left", "diagonal_right"
        ]

    ####################################################
    # Smooth Motion Curve
    ####################################################

    def ease(self, t):
        """Smooth animation curve"""
        return 3 * (t ** 2) - 2 * (t ** 3)

    ####################################################
    # Zoom In
    ####################################################

    def zoom_in(self, clip, duration):
        return clip.resize(
            lambda t: 1 + (self.max_zoom - 1) * self.ease(min(t / duration, 1))
        )

    ####################################################
    # Zoom Out
    ####################################################

    def zoom_out(self, clip, duration):
        return clip.resize(
            lambda t: self.max_zoom - (self.max_zoom - 1) * self.ease(min(t / duration, 1))
        )

    ####################################################
    # Pan Left
    ####################################################

    def pan_left(self, clip, duration):
        return clip.resize(self.max_zoom).set_position(
            lambda t: (-self.pan_distance_x * self.ease(min(t / duration, 1)), "center")
        )

    ####################################################
    # Pan Right
    ####################################################

    def pan_right(self, clip, duration):
        return clip.resize(self.max_zoom).set_position(
            lambda t: (self.pan_distance_x * self.ease(min(t / duration, 1)), "center")
        )

    ####################################################
    # Pan Up
    ####################################################

    def pan_up(self, clip, duration):
        return clip.resize(self.max_zoom).set_position(
            lambda t: ("center", -self.pan_distance_y * self.ease(min(t / duration, 1)))
        )

    ####################################################
    # Pan Down
    ####################################################

    def pan_down(self, clip, duration):
        return clip.resize(self.max_zoom).set_position(
            lambda t: ("center", self.pan_distance_y * self.ease(min(t / duration, 1)))
        )

    ####################################################
    # Diagonal Left
    ####################################################

    def diagonal_left(self, clip, duration):
        return clip.resize(self.max_zoom).set_position(
            lambda t: (
                -self.pan_distance_x * self.ease(min(t / duration, 1)),
                -self.pan_distance_y * self.ease(min(t / duration, 1))
            )
        )

    ####################################################
    # Diagonal Right
    ####################################################

    def diagonal_right(self, clip, duration):
        return clip.resize(self.max_zoom).set_position(
            lambda t: (
                self.pan_distance_x * self.ease(min(t / duration, 1)),
                self.pan_distance_y * self.ease(min(t / duration, 1))
            )
        )

    ####################################################
    # Apply Camera Motion
    ####################################################

    def apply_motion(self, clip, motion, duration):

        motion_map = {
            "zoom_in": self.zoom_in,
            "zoom_out": self.zoom_out,
            "pan_left": self.pan_left,
            "pan_right": self.pan_right,
            "pan_up": self.pan_up,
            "pan_down": self.pan_down,
            "diagonal_left": self.diagonal_left,
            "diagonal_right": self.diagonal_right
        }

        function = motion_map.get(motion)

        if function:
            return function(clip, duration)

        return clip

    ####################################################
    # Main Generator (this was completely missing)
    ####################################################

    def generate_video(self, processed_frames: list) -> str:

        try:

            log_info("Generating cinematic silent video...")

            clips = []
            timeline = 0

            # Total real duration (so final video matches audio length,
            # not shrunk by transition overlaps)
            true_total_duration = sum(
                max(frame["duration"], 1.2) for frame in processed_frames
            )

            last_motion = None

            for index, frame in enumerate(processed_frames):

                duration = max(frame["duration"], 1.2)

                # Use motion from image_processor if present,
                # otherwise pick a random one (avoiding repeat)
                motion = frame.get("motion")

                if not motion or motion == last_motion:
                    motion = random.choice(self.motion_types)
                    while motion == last_motion:
                        motion = random.choice(self.motion_types)

                last_motion = motion

                is_last = (index == len(processed_frames) - 1)

                # Extend duration to compensate for crossfade overlap,
                # so total timeline doesn't shrink
                extended_duration = (
                    duration if is_last
                    else duration + self.transition_duration
                )

                clip = (
                    ImageClip(frame["image"])
                    .set_duration(extended_duration)
                    .resize((VIDEO_WIDTH, VIDEO_HEIGHT))
                )

                clip = self.apply_motion(clip, motion, extended_duration)

                # Subtle camera drift / breathing rotation
                angle = random.uniform(-self.rotation_angle, self.rotation_angle)
                clip = clip.rotate(
                    lambda t, a=angle, d=extended_duration: a * math.sin(2 * math.pi * t / d)
                )

                clip = clip.set_start(timeline)

                transition = frame.get("transition", "crossfade")

                if transition == "crossfade":
                    clip = clip.crossfadein(self.transition_duration)
                elif transition == "fade":
                    clip = clip.fadein(self.transition_duration).fadeout(self.transition_duration)
                elif transition == "dissolve":
                    clip = clip.crossfadein(self.transition_duration * 1.3)

                # Advance timeline by ORIGINAL duration (overlap
                # already compensated via extended_duration above)
                timeline += duration

                clips.append(clip)

            ####################################################
            # Merge All Clips
            ####################################################

            final_clip = CompositeVideoClip(
                clips,
                size=(VIDEO_WIDTH, VIDEO_HEIGHT)
            )

            # Final duration now exactly matches audio length
            final_clip = final_clip.set_duration(true_total_duration)

            ####################################################
            # Export Video
            ####################################################

            create_directory(TEMP_FOLDER)

            output_path = (
                TEMP_FOLDER /
                build_output_filename("temp_video", "mp4")
            )

            final_clip.write_videofile(
                str(output_path),
                codec="libx264",
                fps=self.fps,
                audio=False,
                preset="slow",
                bitrate="8000k",
                ffmpeg_params=["-crf", "17", "-pix_fmt", "yuv420p"],
                threads=4,
                logger=None
            )

            final_clip.close()

            for clip in clips:
                clip.close()

            log_info(f"Video saved : {output_path}")

            return str(output_path)

        except Exception as error:

            log_error(f"Video Generation Failed : {error}")

            raise