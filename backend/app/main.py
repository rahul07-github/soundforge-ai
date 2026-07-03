from fastapi import FastAPI

from app.database.connection import Base, engine

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


from fastapi import FastAPI
from app.api.user import router as user_router

app = FastAPI(title="SoundForge AI")

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "SoundForge AI API is running"}

