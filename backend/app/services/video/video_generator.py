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

        self.rotation_angle= 0.5

    ####################################################
    # Smooth Motion Curve
    ####################################################

    def ease(self, t):

        """
        Smooth animation curve
        """

        return 3 * (t ** 2) - 2 * (t ** 3)

    ####################################################
    # Zoom In
    ####################################################

    def zoom_in(self, clip, duration):

        return clip.resize(

            lambda t:

            1 + (self.max_zoom - 1) *

            self.ease(min(t / duration, 1))

        )

    ####################################################
    # Zoom Out
    ####################################################

    def zoom_out(self, clip, duration):

        return clip.resize(

            lambda t:

            self.max_zoom -

            (self.max_zoom - 1) *

            self.ease(min(t / duration, 1))

        )

    # Pan Left

    def pan_left(self, clip, duration):

        return (

            clip

            .resize(self.max_zoom)

            .set_position(

                lambda t:

                (

                    -self.pan_distance_x *

                    self.ease(min(t / duration, 1)),

                    "center"

                )

            )

        )

    ####################################################
    # Pan Right
    ####################################################

    def pan_right(self, clip, duration):

        return (

            clip

            .resize(self.max_zoom)

            .set_position(

                lambda t:

                (

                    self.pan_distance_x *

                    self.ease(min(t / duration, 1)),

                    "center"

                )

            )

        )

    ####################################################
    # Pan Up
    ####################################################

    def pan_up(self, clip, duration):

        return (

            clip

            .resize(self.max_zoom)

            .set_position(

                lambda t:

                (

                    "center",

                    -self.pan_distance_y *

                    self.ease(min(t / duration, 1))

                )

            )

        )

    ####################################################
    # Pan Down
    ####################################################

    def pan_down(self, clip, duration):

        return (

            clip

            .resize(self.max_zoom)

            .set_position(

                lambda t:

                (

                    "center",

                    self.pan_distance_y *

                    self.ease(min(t / duration, 1))

                )

            )

        )

    ####################################################
    # Diagonal Left
    ####################################################

    def diagonal_left(self, clip, duration):

        return (

            clip

            .resize(self.max_zoom)

            .set_position(

                lambda t:

                (

                    -self.pan_distance_x *

                    self.ease(min(t / duration, 1)),

                    -self.pan_distance_y *

                    self.ease(min(t / duration, 1))

                )

            )

        )

    ####################################################
    # Diagonal Right
    ####################################################

    def diagonal_right(self, clip, duration):

        return (

            clip

            .resize(self.max_zoom)

            .set_position(

                lambda t:

                (

                    self.pan_distance_x *

                    self.ease(min(t / duration, 1)),

                    self.pan_distance_y *

                    self.ease(min(t / duration, 1))

                )

            )

        )

    ####################################################
    # Apply Camera Motion
    ####################################################

    def apply_motion(
        self,clip,motion,duration

    ):

        if motion == "zoom_in":

            return self.zoom_in(clip,duration)

        elif motion == "zoom_out":

            return self.zoom_out(

                clip,

                duration

            )

        elif motion == "pan_left":

            return self.pan_left(

                clip,

                duration

            )

        elif motion == "pan_right":

            return self.pan_right(

                clip,

                duration

            )

        elif motion == "pan_up":

            return self.pan_up(

                clip,

                duration

            )

        elif motion == "pan_down":

            return self.pan_down(
                clip,
                duration
            )

        elif motion == "diagonal_left":

            return self.diagonal_left(

                clip,

                duration

            )

        elif motion == "diagonal_right":

            return self.diagonal_right(

                clip,

                duration

            )

        return clip
    

    def generate_video(self, processed_frames: list) -> str:

        try:

            log_info("Generating cinematic silent video...")

            clips = []
            timeline = 0

            for frame in processed_frames:

                duration = max(
                    frame["duration"],
                    1.5
                )

                clip = (
                    ImageClip(frame["image"])
                    .set_duration(duration)
                    .resize((VIDEO_WIDTH, VIDEO_HEIGHT))
                )

                # Apply camera motion
                clip = self.apply_motion(
                    clip,
                    frame.get("motion"),
                    duration
                )

                # Gentle cinematic zoom
                ####################################################

                zoom_speed = 0.03

                clip = clip.resize(
                    lambda t:
                    1 + zoom_speed *
                    self.ease(min(t / duration, 1))
                )

                ####################################################
                # Small camera drift
                ####################################################

                clip = clip.rotate(
                    lambda t:
                    self.rotation_angle *
                    math.sin(
                        2 * math.pi * t / duration
                    )
                )


                # Apply transition
                transition = frame.get(
                    "transition","crossfade"
                )

                clip = clip.set_start(timeline)

                if transition == "crossfade":
                    clip = (clip.crossfadein(0.5)
                            .fadeout(0.3))
                        

                elif transition == "fade":
                    clip = (clip.fadein(0.5)
                            .fadeout(0.5))
                    
                elif transition =="soft":
                    clip=(clip.fadein(0.25)
                          .fadeout(0.25))
                    
                elif transition =="zoom":
                    clip=(clip.resize(lambda t: 1+ 0.5*(t/duration))
                          .crossfadein(0.5))

                timeline += duration - 0.30
                    

                clips.append(clip)

            ####################################################
            # Merge All Clips
            ####################################################

            final_clip = CompositeVideoClip(
                clips,
                size=(
                    VIDEO_WIDTH,
                    VIDEO_HEIGHT
                )
            )

            final_clip = final_clip.set_duration(
                timeline +
                self.transition_duration
            )

            ####################################################
            # Export Video
            ####################################################

            create_directory(TEMP_FOLDER)

            output_path = (
                TEMP_FOLDER /
                build_output_filename(
                    "temp_video",
                    "mp4"
                )
            )

            final_clip.write_videofile(
                str(output_path),
                codec="libx264",
                fps=self.fps,
                audio=False,
                preset="slow",
                bitrate="8000k",
                audio_codec="aac",
                ffmpeg_params=["-crf","17","-pix_fmt","yuv420p"],
                threads=4,
                logger=None
            )

            final_clip.close()
            for clip in clips:
                clip.close()

            log_info(
                f"Video saved : {output_path}"
            )

            return str(output_path)
        except Exception as error:
            log_error(
                f"Video Generation Failed : {error}"
            )
            raise