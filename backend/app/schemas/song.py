from pydantic import BaseModel
from datetime import datetime


class SongCreate(BaseModel):
    prompt: str


class SongResponse(BaseModel):
    id: int
    user_id: int
    prompt: str
    lyrics: str | None = None
    audio_url: str | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True