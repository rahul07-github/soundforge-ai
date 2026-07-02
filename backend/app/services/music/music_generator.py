from pathlib import Path
import uuid

OUTPUT_DIR = "backend/app/storage/generated/songs"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def generate_music(lyrics: str):

    file_id = str(uuid.uuid4())[:8]

    song_path = f"{OUTPUT_DIR}/{file_id}.mp3"

    with open(song_path, "wb") as f:
        f.write(b"FAKE MP3 DATA")

    return song_path