from pathlib import Path
from gtts import gTTS
import uuid

VOCALS_DIR = Path("backend/app/storage/generated/vocals")
VOCALS_DIR.mkdir(parents=True, exist_ok=True)

def generate_vocal(lyrics: str) -> str:
    if not lyrics or not lyrics.strip():
        lyrics = "This is a generated song by SoundForge AI."

    lyrics = lyrics[:350]

    file_id = str(uuid.uuid4())[:8]
    vocal_path = VOCALS_DIR / f"{file_id}.mp3"

    tts = gTTS(text=lyrics, lang="en")
    tts.save(str(vocal_path))

    return str(vocal_path)