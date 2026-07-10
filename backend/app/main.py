from fastapi import FastAPI

from app.database.connection import Base, engine

from app.models.user import User
from app.models.song import Song
from app.models.history import History

from backend.app.api.lyrics import router as lyrics_router
from backend.app.api.music import router as music_router
from backend.app.api.video import router as video_router
from app.api.user import router as user_router
from app.api.history import router as history_router


app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


app.include_router(lyrics_router)
app.include_router(music_router)
app.include_router(video_router)

app.include_router(user_router)
app.include_router(history_router)


@app.get("/")
def root():
    return {
        "message": "SoundForge AI API is running"
    }