from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text

auth = {
    'user': 'postgres',
    'password': '1234'
}

DATABASE_URL = f"postgresql+psycopg2://{auth['user']}:{auth['password']}@localhost/fitness_booking"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# with engine.connect() as connection:
#     res = connection.execute(text("""
#         SELECT 1 FROM pg_database WHERE datname='fitness_looking'
#     """)).fetchone()
#     if res is None:
#         print("YES")
#         connection.execute(text("""
#             CREATE DATABASE fitness_booking;
#         """))
#         connection.commit()
#     else:
#         print(res)

def get_db():
    """Получение сессии подключения к базе данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if not database_exists(engine.url):
    create_database(engine.url)
