from backend.app.services.lyrics.model_loader import lyrics_model
from backend.app.services.lyrics.prompt import build_prompt
from backend.app.services.music.music_generator import generate_music

from pathlib import Path
import uuid
import json

LYRICS_DIR = "backend/app/storage/generated/lyrics"
METADATA_DIR = "backend/app/storage/generated/metadata"

Path(LYRICS_DIR).mkdir(parents=True, exist_ok=True)
Path(METADATA_DIR).mkdir(parents=True, exist_ok=True)


def generate_lyrics(user_prompt: str):

    prompt = build_prompt(user_prompt)

    result = lyrics_model(
        prompt,
        max_length=150,
        truncation=True,
        num_return_sequences=1
    )

    generated_text = result[0]["generated_text"]

    lyrics = generated_text.replace(prompt, "").strip()

    file_id = str(uuid.uuid4())[:8]

    # SAVE LYRICS
    lyrics_path = f"{LYRICS_DIR}/{file_id}.txt"

    with open(lyrics_path, "w", encoding="utf-8") as f:
        f.write(lyrics)

    # GENERATE MUSIC
    song_path = generate_music(lyrics)

    # SAVE METADATA
    metadata = {
        "id": file_id,
        "prompt": user_prompt,
        "lyrics_path": lyrics_path,
        "song_path": song_path
    }

    metadata_path = f"{METADATA_DIR}/{file_id}.json"

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    return {
        "lyrics": lyrics,
        "lyrics_path": lyrics_path,
        "metadata_path": metadata_path,
        "song_path": song_path
    }