from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

from app.database.connection import Base



class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    genre = Column(String(100))
    file_url = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"))