from sqlalchemy import text

from app.database import get_db


def create_procedures():
    with next(get_db()) as db:
        db.execute(text("""
            CREATE OR REPLACE PROCEDURE add_user(name TEXT, phone TEXT, role TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO users (name, phone, role) VALUES (name, phone, role);
            END;
            $$;
        """))

        db.execute(text("""
            CREATE OR REPLACE PROCEDURE delete_service(service_name TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                DELETE FROM services WHERE service_name = service_name;
            END;
            $$;
        """))
        db.commit()
