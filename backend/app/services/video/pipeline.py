import json
from pathlib import Path
from datetime import datetime

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.validators import validate_audio
from backend.app.utils.file_manager import create_directory
from backend.app.utils.constants import ( METADATA_FOLDER, SUBTITLE_FOLDER,ENABLES_SUBTITLES)

from backend.app.services.video.beat_detector import BeatDetector
from backend.app.services.video.frame_generator import FrameGenerator
from backend.app.services.video.image_processor import ImageProcessor
from backend.app.services.video.video_generator import VideoGenerator
from backend.app.services.video.audio_merger import AudioMerger
from backend.app.services.video.video_export import VideoExporter
from backend.app.services.video.thumbnail_generator import ThumbnailGenerator
from backend.app.services.video.subtitle_generator import SubtitleGenerator
from backend.app.services.video.subtitle_burner import SubtitleBurner

# yw wale import specific humne jo images liye h uske liye h ------
from backend.app.services.video.scene_loader import SceneLoader
from backend.app.services.video.audio_trimmer import AudioTrimmer

class VideoPipeline:
    """
    Main Video Pipeline Controller
    Handles the complete AI video generation workflow.
    """

    def __init__(self):

        self.beat_detector = BeatDetector()
        self.frame_generator = FrameGenerator()
        self.image_processor = ImageProcessor()
        self.video_generator = VideoGenerator()
        self.audio_merger = AudioMerger()
        self.video_exporter = VideoExporter()
        self.thumbnail_generator = ThumbnailGenerator()
        self.subtitle_generator = SubtitleGenerator()
        self.subtitle_burner = SubtitleBurner()
        self.scene_loader = SceneLoader()
        self.audio_trimmer = AudioTrimmer()


    def generate_video(self, song_id: str):
        """Execute complete video generation pipeline.
        """
        try:

            log_info(f"Starting Video Pipeline : {song_id}")

            # STEP 1 : Read Metadata
            metadata = self.read_metadata(song_id)
            
            # STEP 2 : Read Required Paths
            song_path = metadata["song_path"]
            lyrics_path = metadata["lyrics_path"]
            cover_path = metadata["cover_path"]

            
            # STEP 3 : Validate Song

            validate_audio(song_path)

            # Step 4 Trim audio

            trimmed_audio = self.audio_trimmer.trim_audio(
                song_path=song_path,
                start_time=30,
                duration=20
            )

            
            # STEP 4 : Beat Detection

            beat_data = self.beat_detector.detect_beats(trimmed_audio)
            
            # STEP 5 : Frame Generation

            frames = self.frame_generator.generate_frames(
                beat_data
            )
            ## Load Scene Images 
            scene_images = self.scene_loader.load_images()

            # STEP 6 : Image Processing
            scene_images = self.scene_loader.load_images()

            processed_frames = self.image_processor.process_images(
                frames,
                scene_images
#               cover_path
            )

            # STEP 7 : Generate Silent Video

            silent_video = self.video_generator.generate_video(
                processed_frames
            )

            # STEP 8 : Merge Audio

            merged_video = self.audio_merger.merge_audio(
                silent_video,
                trimmed_audio
            )
            # STEP 9 : Generate Subtitle

            subtitle_path = None

            if ENABLES_SUBTITLES:

                create_directory(SUBTITLE_FOLDER)

                subtitle_path = (
                    self.subtitle_generator.generate_subtitle(
                        lyrics_path=lyrics_path,
                        output_path=str(
                            SUBTITLE_FOLDER / f"{song_id}.srt"
                        )
                    )
                )

            # STEP 10 : Burn Subtitle Into Video   

            if ENABLES_SUBTITLES:

                burned_video = self.subtitle_burner.burn_subtitles(
                    video_path=merged_video,
                    subtitle_path=subtitle_path
                )

            else:
                burned_video = merged_video

            # STEP 11 : Export Final Video
            exported_video = self.video_exporter.export_video(
                burned_video
            )
            
        
            # STEP 12 : Generate Thumbnail

            thumbnail_path = (
                self.thumbnail_generator.generate_thumbnail(
                    exported_video
                )
            )
            # STEP 13 : Update Metadata

            self.update_metadata(
                song_id=song_id,
                video_path=exported_video,
                thumbnail_path=thumbnail_path,
                subtitle_path=subtitle_path,
                clip_start=30,
                clip_end=50
            )

            # STEP 14 : Success
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
        """
        Read metadata generated by Lyrics/Music Module.
        """

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

            metadata = json.load(file)

        return metadata
    
    def update_metadata(
        self,
        song_id: str,
        video_path: str,
        thumbnail_path: str,
        subtitle_path: str,
        clip_start: int,
        clip_end: int
):
        """
        Update metadata after successful video generation.
        """

        metadata_file = METADATA_FOLDER / f"{song_id}.json"

        with open(
            metadata_file,
            "r",
            encoding="utf-8"
        ) as file:

            metadata = json.load(file)

        metadata["video_path"] = video_path
        metadata["thumbnail_path"] = thumbnail_path
        metadata["subtitle_path"] = subtitle_path if ENABLES_SUBTITLES else None
        metadata["clip_start"] = clip_start
        metadata["clip_end"] = clip_end
        metadata["clip_duration"] = clip_end - clip_start
        metadata["status"] = "completed"
        metadata["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        log_info("Metadata updated successfully.")