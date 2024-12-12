from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/fitness_booking"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Получение сессии подключения к базе данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
