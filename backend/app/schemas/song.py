from pydantic import BaseModel


class SongCreate(BaseModel):
    title: str
    artist: str
    genre: str
    file_url: str


class SongResponse(BaseModel):
    id: int
    title: str
    artist: str
    genre: str
    file_url: str
    user_id: int

    class Config:
        from_attributes = True