from fastapi import FastAPI

from app.database.db import Base, engine

from app.models.user import User
from app.models.song import Song
from app.models.history import History 

app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Welcome to SoundForge AI"
        
    }

