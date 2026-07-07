from pathlib import Path
import uuid
import json
from backend.app.services.music.custom_voice import get_custom_voice
from backend.app.services.lyrics.model_loader import lyrics_model
from backend.app.services.lyrics.prompt import build_prompt
from backend.app.services.music.vocal_generator import generate_vocal
from backend.app.services.music.cover_generator import generate_cover
from backend.app.services.music.audio_mixer import mix_audio

LYRICS_DIR = Path("backend/app/storage/generated/lyrics")
METADATA_DIR = Path("backend/app/storage/generated/metadata")
SONGS_DIR = Path("backend/app/storage/generated/songs")

LYRICS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)
SONGS_DIR.mkdir(parents=True, exist_ok=True)

def select_beat(user_prompt: str) -> str:
    p = user_prompt.lower()

    if "sad" in p or "breakup" in p or "cry" in p:
        return "backend/app/storage/generated/assets/beats/sad.mp3"
    if "love" in p or "romantic" in p:
        return "backend/app/storage/generated/assets/beats/romantic.mp3"
    if "rap" in p or "hip hop" in p:
        return "backend/app/storage/generated/assets/beats/rap.mp3"

    return "backend/app/storage/generated/assets/beats/pop.mp3"

def clean_lyrics(text: str, user_prompt: str) -> str:
    bad = ["http", "www", ".com", "/r/", "reddit", "iframe", "quickship"]

    if not text or any(x in text.lower() for x in bad):
        return f"""[Verse 1]
This song is about {user_prompt}
Feelings moving through the night
Every heartbeat finds a rhythm
Every dream becomes a light

[Chorus]
Let the music play tonight
Let the words and beats unite
Every sound and every line
Turns this moment into life
"""

    return text.strip()

def generate_lyrics(user_prompt: str):
    prompt = build_prompt(user_prompt)

    result = lyrics_model(
        prompt,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.85,
        top_p=0.92,
        repetition_penalty=1.2,
        truncation=True,
        num_return_sequences=1
    )

    generated_text = result[0]["generated_text"]
    lyrics = generated_text.replace(prompt, "").strip()
    lyrics = clean_lyrics(lyrics, user_prompt)

    file_id = str(uuid.uuid4())[:8]

    lyrics_path = LYRICS_DIR / f"{file_id}.txt"
    with open(lyrics_path, "w", encoding="utf-8") as f:
        f.write(lyrics)

    vocal_path = generate_vocal(lyrics)
    beat_path = select_beat(user_prompt)

    song_path = SONGS_DIR / f"{file_id}.mp3"
    mix_audio(vocal_path, beat_path, str(song_path))

    cover_path = generate_cover(user_prompt)

    metadata_path = METADATA_DIR / f"{file_id}.json"
    metadata = {
        "id": file_id,
        "prompt": user_prompt,
        "duration": "20 sec",
        "lyrics_path": str(lyrics_path),
        "vocal_path": str(vocal_path),
        "beat_path": beat_path,
        "song_path": str(song_path),
        "cover_path": str(cover_path),
        "metadata_path": str(metadata_path)
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    return metadata | {"lyrics": lyrics}