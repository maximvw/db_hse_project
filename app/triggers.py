from sqlalchemy import text


def create_triggers(engine):
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE OR REPLACE FUNCTION calculate_total_cost()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.total_cost := (
                    SELECT s.price_per_hour * 
                        EXTRACT(EPOCH FROM (sch.end_time - sch.start_time)) / 3600
                    FROM schedule sch
                    JOIN services s ON s.id = sch.service_id
                    WHERE sch.id = NEW.schedule_id
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """))

        connection.execute(text("""
            CREATE TRIGGER trigger_calculate_total_cost
            BEFORE INSERT OR UPDATE ON bookings
            FOR EACH ROW
            EXECUTE FUNCTION calculate_total_cost();
        """))
