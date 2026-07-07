from pathlib import Path
from pydub import AudioSegment
import uuid

FFMPEG_PATH = r"E:\ffmpeg2\bin\ffmpeg.exe"
FFPROBE_PATH = r"E:\ffmpeg2\bin\ffprobe.exe"

AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH

SONGS_DIR = Path("backend/app/storage/generated/songs")
SONGS_DIR.mkdir(parents=True, exist_ok=True)


def select_beat(prompt: str):

    prompt = prompt.lower()

    if "sad" in prompt or "breakup" in prompt or "cry" in prompt:
        return "backend/app/storage/generated/assets/beats/sad.mp3"

    elif "love" in prompt or "romantic" in prompt:
        return "backend/app/storage/generated/assets/beats/romantic.mp3"

    elif "rap" in prompt or "hip hop" in prompt:
        return "backend/app/storage/generated/assets/beats/rap.mp3"

    else:
        return "backend/app/storage/generated/assets/beats/pop.mp3"


def generate_music(prompt: str):

    beat_path = select_beat(prompt)

    print("Selected Beat:", beat_path)

    beat = AudioSegment.from_file(beat_path)

    duration = 20000

    while len(beat) < duration:
        beat += beat

    beat = beat[:duration]

    file_id = str(uuid.uuid4())[:8]

    song_path = SONGS_DIR / f"{file_id}.mp3"

    beat.export(song_path, format="mp3")

    return {
        "song_path": str(song_path),
        "beat_path": beat_path
    }