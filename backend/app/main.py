from fastapi import FastAPI
from backend.app.api.music import router as music_router
from backend.app.api.lyrics import router as lyrics_router

app = FastAPI()

app.include_router(lyrics_router)
app.include_router(music_router)