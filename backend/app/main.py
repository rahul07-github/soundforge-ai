from fastapi import FastAPI

from backend.app.database.db import Base, engine

from backend.app.models.user import User
from backend.app.models.song import Song
from backend.app.models.history import History

from backend.app.api.lyrics import router as lyrics_router
from backend.app.api.music import router as music_router

app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(lyrics_router)
app.include_router(music_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to SoundForge AI"
    }