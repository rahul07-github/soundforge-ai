from sqlalchemy import Column, Integer, String, ForeignKey
<<<<<<< HEAD
from app.database.connection import Base
=======
from backend.app.database.db import Base
>>>>>>> 98206143fd798188b384dc908535371470f8d1d7


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    genre = Column(String(100))
    file_url = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"))