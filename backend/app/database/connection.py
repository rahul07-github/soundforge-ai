from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

<<<<<<< HEAD
DATABASE_URL = "mysql+pymysql://root:1234@localhost/soundforge_ai"
=======
DATABASE_URL = "mysql+pymysql://root:123456@localhost/soundforge_ai"
>>>>>>> origin

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()