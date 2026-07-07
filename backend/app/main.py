from fastapi import FastAPI

from app.database.connection import Base, engine


from app.models.user import User
from app.models.song import Song
from app.models.history import History


from app.api.user import router as user_router
# from app.api.lyrics import router as lyrics_router
# from app.api.music import router as music_router

app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router)
# app.include_router(lyrics_router)
# app.include_router(music_router)


@app.get("/")
def root():
    return {
        "message": "SoundForge AI API is running"
    }