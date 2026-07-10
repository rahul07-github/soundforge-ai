import json
from pathlib import Path
from datetime import datetime

from pydub import AudioSegment

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.validators import validate_audio
from backend.app.utils.file_manager import create_directory
from backend.app.utils.constants import (METADATA_FOLDER, SUBTITLE_FOLDER, ENABLES_SUBTITLES)

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
from backend.app.services.video.audio_trimmer import AudioTrimmer


class VideoPipeline:
    """
    Main Video Pipeline Controller
    Handles the complete AI video generation workflow.
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
        self.image_processor = ImageProcessor()
        self.video_generator = VideoGenerator()
        self.audio_merger = AudioMerger()
        self.video_exporter = VideoExporter()
        self.thumbnail_generator = ThumbnailGenerator()
        self.subtitle_generator = SubtitleGenerator()
        self.subtitle_burner = SubtitleBurner()

    def generate_video(self, song_id: str):
        """Execute complete video generation pipeline."""
        try:
            log_info(f"Starting Video Pipeline : {song_id}")

            # STEP 1 : Read Metadata
            metadata = self.read_metadata(song_id)

            # STEP 1.5 : Detect Mood
            mood = self.mood_detector.detect_mood(metadata)

            # STEP 1.6 : Select Categories
            selected_categories = self.category_selector.select_categories(mood)

            log_info(f"Selected Categories : {selected_categories}")

            # STEP 2 : Read Required Paths
            song_path = metadata["song_path"]
            lyrics_path = metadata["lyrics_path"]
            cover_path = metadata["cover_path"]

            # STEP 3 : Validate Song
            validate_audio(song_path)

            # STEP 4 : Trim Audio (auto-detect based on song length)
            trimmed_audio = self.audio_trimmer.trim_audio(
                song_path=song_path
            )

            # STEP 5 : Beat Detection
            beat_data = self.beat_detector.detect_beats(trimmed_audio)

            # STEP 6 : Frame Generation
            frames = self.frame_generator.generate_frames(beat_data)

            # STEP 7 : Load Scene Images
            datasets = self.dataset_loader.load_datasets(selected_categories)

            # STEP 8 : Mix Images
            mixed_images = self.image_mixer.mix_images(datasets, len(frames))

            # STEP 9 : Schedule Images to Frames
            scheduled_images = self.image_scheduler.schedule_images(
                frames,
                mixed_images
            )

            log_info(f"{len(scheduled_images)} image scheduled")

            # STEP 10 : Image Processing
            processed_frames = self.image_processor.process_images(scheduled_images)

            # STEP 11 : Generate Silent Video
            silent_video = self.video_generator.generate_video(processed_frames)

            # STEP 12 : Merge Audio
            merged_video = self.audio_merger.merge_audio(
                silent_video,
                trimmed_audio
            )

            # STEP 13 : Generate Subtitle
            subtitle_path = None

            if ENABLES_SUBTITLES:
                create_directory(SUBTITLE_FOLDER)

                subtitle_path = (
                    self.subtitle_generator.generate_subtitle(
                        lyrics_path=lyrics_path,
                        output_path=str(SUBTITLE_FOLDER / f"{song_id}.srt")
                    )
                )

            # STEP 14 : Burn Subtitle Into Video
            if ENABLES_SUBTITLES:
                burned_video = self.subtitle_burner.burn_subtitles(
                    video_path=merged_video,
                    subtitle_path=subtitle_path
                )
            else:
                burned_video = merged_video

            # STEP 15 : Export Final Video
            exported_video = self.video_exporter.export_video(burned_video)

            # STEP 16 : Generate Thumbnail
            thumbnail_path = (
                self.thumbnail_generator.generate_thumbnail(exported_video)
            )

            # STEP 17 : Get Actual Trimmed Clip Duration (for metadata)
            trimmed_clip_duration = len(
                AudioSegment.from_file(trimmed_audio)
            ) / 1000

            # STEP 18 : Update Metadata
            self.update_metadata(
                song_id=song_id,
                video_path=exported_video,
                thumbnail_path=thumbnail_path,
                subtitle_path=subtitle_path,
                clip_duration=trimmed_clip_duration
            )

            # STEP 19 : Success
            log_info("Video Generation Completed Successfully")

            return {
                "song_id": song_id,
                "video_path": exported_video,
                "thumbnail_path": thumbnail_path,
                "subtitle_path": subtitle_path
            }

        except Exception as error:
            log_error(f"Pipeline Error : {error}")
            raise

    def read_metadata(self, song_id: str):
        """Read metadata generated by Lyrics/Music Module."""

        metadata_file = METADATA_FOLDER / f"{song_id}.json"

        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Metadata file not found : {metadata_file}"
            )

        with open(metadata_file, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        return metadata

    def update_metadata(
        self,
        song_id: str,
        video_path: str,
        thumbnail_path: str,
        subtitle_path: str,
        clip_duration: float
    ):
        """Update metadata after successful video generation."""

        metadata_file = METADATA_FOLDER / f"{song_id}.json"

        with open(metadata_file, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        metadata["video_path"] = video_path
        metadata["thumbnail_path"] = thumbnail_path
        metadata["subtitle_path"] = subtitle_path if ENABLES_SUBTITLES else None
        metadata["clip_duration"] = round(clip_duration, 2)
        metadata["status"] = "completed"
        metadata["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(metadata_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

        log_info("Metadata updated successfully.")