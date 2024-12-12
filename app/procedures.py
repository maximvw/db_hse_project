from sqlalchemy import text


def create_procedures(engine):
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE OR REPLACE PROCEDURE add_user(name TEXT, phone TEXT, role TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO users (name, phone, role) VALUES (name, phone, role);
            END;
            $$;
        """))

        connection.execute(text("""
            CREATE OR REPLACE PROCEDURE delete_service(service_name TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                DELETE FROM services WHERE service_name = service_name;
            END;
            $$;
        """))
