from fastapi import FastAPI

from app.database.connection import Base, engine

from app.models.user import User
from app.models.song import Song
from app.models.history import History
from app.models.subscription import Subscription
from app.api import subscription

from app.api import payment

from app.api.user import router as user_router
from app.api.history import router as history_router

app = FastAPI(
    title="SoundForge AI API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(history_router)
app.include_router(subscription.router)
app.include_router(payment.router)


@app.get("/")
def root():
    return {
        "message": "SoundForge AI API is running"
    }



