import json
from pathlib import Path
from datetime import datetime

from pydub import AudioSegment

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.validators import validate_audio
from backend.app.utils.file_manager import create_directory
from backend.app.utils.constants import (
    METADATA_FOLDER,SUBTITLE_FOLDER,ENABLES_SUBTITLES)

from backend.app.services.video.beat_detector import BeatDetector
from backend.app.services.video.frame_generator import FrameGenerator
from backend.app.services.video.image_processor import ImageProcessor
from backend.app.services.video.video_generator import VideoGenerator
from backend.app.services.video.audio_merger import AudioMerger
from backend.app.services.video.video_export import VideoExporter
from backend.app.services.video.thumbnail_generator import ThumbnailGenerator
from backend.app.services.video.subtitle_generator import SubtitleGenerator
from backend.app.services.video.subtitle_burner import SubtitleBurner

from backend.app.services.video.dataset_loader import DatasetLoader
from backend.app.services.video.image_mixer import ImageMixer
from backend.app.services.video.image_scheduler import ImageScheduler
from backend.app.services.video.mood_detector import MoodDetector
from backend.app.services.video.category_selector import CategorySelector
from backend.app.services.video.scene_planner import ScenePlanner
from backend.app.services.video.audio_trimmer import AudioTrimmer
from backend.app.services.video.prompt_builder import PromptBuilder


class VideoPipeline:
    """
    Main Video Pipeline Controller
    """

    def __init__(self):

        self.beat_detector = BeatDetector()
        self.frame_generator = FrameGenerator()
        self.audio_trimmer = AudioTrimmer()

        self.dataset_loader = DatasetLoader()
        self.image_mixer = ImageMixer()
        self.image_scheduler = ImageScheduler()

        self.mood_detector = MoodDetector()
        self.category_selector = CategorySelector()
        self.scene_planner = ScenePlanner()

        self.image_processor = ImageProcessor()
        self.video_generator = VideoGenerator()
        self.audio_merger = AudioMerger()
        self.video_exporter = VideoExporter()
        self.thumbnail_generator = ThumbnailGenerator()
        self.subtitle_generator = SubtitleGenerator()
        self.subtitle_burner = SubtitleBurner()
        self.prompt_builder = PromptBuilder()



    def generate_video(self, song_id: str):

        try:

            log_info(f"Starting Video Pipeline : {song_id}")

            ####################################################
            # STEP 1 : Read Metadata
            ####################################################

            metadata = self.read_metadata(song_id)

            ####################################################
            # STEP 2 : Detect Mood
            ####################################################

            mood = self.mood_detector.detect_mood(metadata)

            ####################################################
            # STEP 3 : Select Categories
            ####################################################

            selected_categories = self.category_selector.select_categories(
                mood
            )

            log_info(
                f"Selected Categories : {selected_categories}"
            )

            scene_prompts = {}

            for scene in scenes:

                scene_prompts[scene["scene_id"]] = self.prompt_builder.build_prompt(
                    mood=scene["mood"],
                    category=scene["category"],
                    energy=scene["energy"]
                )
            # STEP 4 : Paths
            
            song_path = metadata["song_path"]
            lyrics_path = metadata["lyrics_path"]

            # STEP 5 : Validate Audio

            validate_audio(song_path)

            # STEP 6 : Trim Audio
            

            trimmed_audio = self.audio_trimmer.trim_audio(
                song_path=song_path
            )

            # STEP 7 : Beat Detection
            

            beat_data = self.beat_detector.detect_beats(
                trimmed_audio
            )

            ####################################################
            # STEP 8 : Scene Planning
            ####################################################

            scenes = self.scene_planner.create_scenes(
                beat_data=beat_data,
                categories=selected_categories
            )
            for scene in scenes:
                log_info(
                    f"Scene {scene['scene_id']} | "
                    f"{scene['category']} | "
                    f"{scene['start_time']:.2f}s - "
                    f"{scene['end_time']:.2f}s"
                )

            ####################################################
            # STEP 9 : Frame Generation
            ####################################################

            frames = self.frame_generator.generate_frames(
                beat_data
            )

            ####################################################
            # STEP 10 : Dataset Loading
            ####################################################

            datasets = self.dataset_loader.load_datasets(
                selected_categories
            )

            # STEP 10 : Build CLIP Prompts

            scene_prompts = {

                "nature":
                "Beautiful cinematic nature landscape with realistic lighting",

                "forest":
                "Dense green forest with warm sunlight",

                "mountains":
                "Snow covered mountains during golden hour",

                "sunset":
                "Golden sunset over mountains with cinematic colors",

                "romantic":
                "Romantic evening with soft golden lighting",

                "sad":
                "Rainy lonely landscape with dramatic atmosphere",

                "lofi":
                "Peaceful urban evening with cozy lo-fi mood"

            }
            # STEP 11 : Image Mixing

            mixed_images = self.image_mixer.mix_images(
                datasets,
                frame_count= len(frames),
                prompts=scene_prompts
            )

            ####################################################
            # STEP 12 : Image Scheduling
            ####################################################

            scheduled_images = self.image_scheduler.schedule_images(
                frames,
                mixed_images
            )

            ####################################################
            # STEP 13 : Image Processing
            ####################################################

            processed_frames = self.image_processor.process_images(
                scheduled_images
            )

            ####################################################
            # STEP 14 : Silent Video
            ####################################################

            silent_video = self.video_generator.generate_video(
                processed_frames
            )

            ####################################################
            # STEP 15 : Merge Audio
            ####################################################

            merged_video = self.audio_merger.merge_audio(
                silent_video,
                trimmed_audio
            )

            ####################################################
            # STEP 16 : Subtitle
            ####################################################

            subtitle_path = None

            if ENABLES_SUBTITLES:

                create_directory(
                    SUBTITLE_FOLDER
                )

                subtitle_path = (
                    self.subtitle_generator.generate_subtitle(
                        lyrics_path=lyrics_path,
                        output_path=str(
                            SUBTITLE_FOLDER /
                            f"{song_id}.srt"
                        )
                    )
                )

            ####################################################
            # STEP 17 : Burn Subtitle
            ####################################################

            if ENABLES_SUBTITLES:

                final_video = (
                    self.subtitle_burner.burn_subtitles(
                        video_path=merged_video,
                        subtitle_path=subtitle_path
                    )
                )

            else:

                final_video = merged_video

            ####################################################
            # STEP 18 : Export
            ####################################################

            exported_video = (
                self.video_exporter.export_video(
                    final_video
                )
            )

            ####################################################
            # STEP 19 : Thumbnail
            ####################################################

            thumbnail_path = (
                self.thumbnail_generator.generate_thumbnail(
                    exported_video
                )
            )

            ####################################################
            # STEP 20 : Metadata
            ####################################################

            clip_duration = (
                len(AudioSegment.from_file(trimmed_audio))
                / 1000
            )

            self.update_metadata(
                song_id=song_id,
                video_path=exported_video,
                thumbnail_path=thumbnail_path,
                subtitle_path=subtitle_path,
                clip_duration=clip_duration
            )

            log_info(
                "Video Generation Completed Successfully"
            )

            return {

                "song_id": song_id,

                "video_path": exported_video,

                "thumbnail_path": thumbnail_path,

                "subtitle_path": subtitle_path

            }

        except Exception as error:

            log_error(
                f"Pipeline Error : {error}"
            )

            raise

    def read_metadata(self, song_id: str):

        metadata_file = METADATA_FOLDER / f"{song_id}.json"

        if not metadata_file.exists():

            raise FileNotFoundError(
                f"Metadata file not found : {metadata_file}"
            )

        with open(
            metadata_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def update_metadata(
        self,
        song_id,
        video_path,
        thumbnail_path,
        subtitle_path,
        clip_duration
    ):
        metadata_file = METADATA_FOLDER / f"{song_id}.json"

        with open(
            metadata_file,
            "r",
            encoding="utf-8"
        ) as file:
            metadata = json.load(file)

        metadata["video_path"] = video_path
        metadata["thumbnail_path"] = thumbnail_path
        metadata["subtitle_path"] = (
            subtitle_path if ENABLES_SUBTITLES else None
        )
        metadata["clip_duration"] = round(
            clip_duration,
            2
        )
        metadata["status"] = "completed"
        metadata["generated_at"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )
        log_info(
            "Metadata updated successfully."
        )