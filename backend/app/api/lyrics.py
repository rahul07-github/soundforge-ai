from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.lyrics.lyrics_generator import generate_lyrics

router = APIRouter()


class LyricsRequest(BaseModel):
    prompt: str


@router.post("/generate-lyrics")
def generate_lyrics_api(request: LyricsRequest):
    result = generate_lyrics(request.prompt)
    return result