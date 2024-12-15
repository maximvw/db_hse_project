from sqlalchemy import text

from app.database import get_db


def create_tables():
    with next(get_db()) as db:
        db.execute(text("""
            DROP TABLE users CASCADE;
            DROP TABLE services CASCADE;
            DROP TABLE schedule CASCADE;
            DROP TABLE bookings CASCADE;
        """))


        db.execute(text("""
            CREATE TABLE if not exists users(
                id bigserial PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                role VARCHAR(15) NOT NULL
            );


            CREATE TABLE if not exists services(
                id bigserial PRIMARY KEY,
                service_name VARCHAR(255) NOT NULL UNIQUE,
                price_per_hour INTEGER NOT NULL
            );

            CREATE TABLE if not exists schedule(
                id bigserial PRIMARY KEY,
                trainer_id INT NOT NULL,
                service_id INT NOT NULL,
                date_calendar DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                FOREIGN KEY (trainer_id) REFERENCES Users(id) ON DELETE CASCADE,
                FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE
            );

            CREATE TABLE if not exists bookings(
                id bigserial PRIMARY KEY,
                client_id INT NOT NULL,
                schedule_id INT NOT NULL,
                total_cost DECIMAL(10, 2) DEFAULT 0,
                FOREIGN KEY (client_id) REFERENCES Users(id) ON DELETE CASCADE,
                FOREIGN KEY (schedule_id) REFERENCES Schedule(id) ON DELETE CASCADE
            );

            CREATE INDEX if not exists idx_service_name ON services(service_name);
        """))

        db.commit()
