from sqlalchemy import Column, Integer, String
<<<<<<< HEAD
from app.database.connection import Base
=======
from backend.app.database.db import Base
>>>>>>> 98206143fd798188b384dc908535371470f8d1d7

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)