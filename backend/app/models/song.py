from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

<<<<<<< HEAD
from backend.app.database.connection import Base 
=======
from app.database.connection import Base 
>>>>>>> origin
from sqlalchemy.orm import relationship


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    prompt = Column(Text, nullable=False)

    lyrics = Column(Text, nullable=True)

    audio_url = Column(String(500), nullable=True)

    status = Column(String(50), default="pending")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    user = relationship("User", back_populates="songs") 
    history = relationship(
    "History",
    back_populates="song"
)