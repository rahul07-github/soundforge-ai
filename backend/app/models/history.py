from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

<<<<<<< HEAD
from backend.app.database.connection import Base
=======
from app.database.connection import Base
>>>>>>> origin


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    song_id = Column(
        Integer,
        ForeignKey("songs.id"),
        nullable=False
    )

    action = Column(
        String(100),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="history"
    )

    song = relationship(
        "Song",
        back_populates="history"
    )