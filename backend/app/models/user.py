from sqlalchemy import Column, Integer, String
from app.database.connection import Base 
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    songs = relationship("Song", back_populates="user")
    history = relationship(
    "History",
    back_populates="user"
)