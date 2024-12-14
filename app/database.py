from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

auth = {
    'user': 'postgres',
    'password': '1234'
}

DATABASE_URL = f"postgresql+psycopg2://{auth['user']}:{auth['password']}@localhost/fitness_booking"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Получение сессии подключения к базе данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if not database_exists(engine.url):
    create_database(engine.url)
