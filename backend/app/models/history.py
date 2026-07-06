from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
<<<<<<< HEAD
from app.database.connection import Base
=======
from backend.app.database.db import Base
>>>>>>> 98206143fd798188b384dc908535371470f8d1d7


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    song_id = Column(Integer, ForeignKey("songs.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())