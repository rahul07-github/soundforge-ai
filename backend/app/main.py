from fastapi import FastAPI


app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to SoundForge AI"
    
    } 



from fastapi import FastAPI

from backend.app.api.lyrics import router as lyrics_router
from backend.app.api.music import router as music_router

app = FastAPI()

app.include_router(lyrics_router)
app.include_router(music_router)


