from fastapi import FastAPI


from app.database.db import Base, engine
from app.models.user import User
from app.models.song import Song
from app.models.history import History


from backend.app.api.music import router as music_router

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

app.include_router(lyrics_router)
app.include_router(music_router)

