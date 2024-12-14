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


            CREATE OR REPLACE PROCEDURE add_service(name TEXT, price TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO services (service_name, price_per_hour) VALUES (name, price);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE add_schedule(trainer_id INTEGER, service_id INTEGER, date_calendar DATE
                                                     start_time TIME, end_time TIME)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO schedule (trainer_id, service_id, date_calendar, start_time, end_time)
                              VALUES (trainer_id, service_id, date_calendar, start_time, end_time);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE add_booking(client_id INTEGER, schedule_id INTEGER)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO bookings (client_id, schedule_id)
                              VALUES (trainer_id, service_id);
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


        db.execute(text("""
            CREATE OR REPLACE PROCEDURE delete_service(service_name TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                DELETE FROM services WHERE service_name = service_name;
            END;
            $$;
        """))
        db.commit()
