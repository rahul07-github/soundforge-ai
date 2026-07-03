from fastapi import FastAPI
from backend.app.api.lyrics import router as lyrics_router
from backend.app.api.music import router as music_router

app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(lyrics_router)