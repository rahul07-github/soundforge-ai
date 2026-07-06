from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.lyrics.lyrics_generator import generate_lyrics

router = APIRouter()


class LyricsRequest(BaseModel):
    prompt: str


@router.post("/generate-lyrics")
def generate_lyrics_api(request: LyricsRequest):

    result = generate_lyrics(request.prompt)

    return {
    "status": "success",
    "prompt": request.prompt,
    "lyrics_file": result["lyrics_path"],
    "song_file": result["song_path"],
    "metadata_file": result["metadata_path"]
}
@router.get("/songs")
def get_songs():

    db = SessionLocal()

    songs = db.query(Song).all()

    result = []

    for song in songs:
        result.append({
            "id": song.id,
            "prompt": song.prompt,
            "lyrics_path": song.lyrics_path,
            "song_path": song.song_path,
            "metadata_path": song.metadata_path
        })

    db.close()

    return result