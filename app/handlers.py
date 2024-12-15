from datetime import date, time

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import User, Service, Schedule, Booking


def add_user(db: Session, name: str, phone: str, role: str):
    try:
        db.execute(text("CALL add_user(:name, :phone, :role)"), {"name": name, "phone": phone, "role": role})
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_service(db: Session, name: str, price: int):
    try:
        db.execute(text("CALL add_service(:name, :price)"), {"name": name, "price": price})
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_schedule(db: Session, trainer_id: int, service_id: int, date_calendar: date, start_time: time, end_time: time):
    try:
        db.execute(text("CALL add_schedule(:trainer_id, :service_id, :date_calendar, :start_time, :end_time)"),
                   {"trainer_id": trainer_id, "service_id": service_id, "date_calendar": date_calendar,
                    "start_time": start_time, "end_time": end_time})
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_booking(db: Session, client_id: int, schedule_id: int, total_cost: float = 0):
    try:
        db.execute(text("CALL add_booking(:client_id, :schedule_id)"),
                   {"client_id": client_id, "schedule_id": schedule_id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def get_users(db: Session):
    return db.query(User).all()

def get_table_data(db: Session, table_name: str):
    return db.execute(text(f"SELECT * FROM {table_name}")).fetchall()


def clear_tables(db: Session):
    try:
        db.execute(text("""
            TRUNCATE TABLE users CASCADE;
            TRUNCATE TABLE services CASCADE;
            TRUNCATE TABLE schedule CASCADE;
            TRUNCATE TABLE bookings CASCADE;
        """))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_booking(db: Session):
    try:
        db.execute(text("""
            TRUNCATE TABLE bookings CASCADE;
        """))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_schedule(db: Session):
    try:
        db.execute(text("""
            TRUNCATE TABLE schedule CASCADE;
        """))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_user(db: Session):
    try:
        db.execute(text("""
            TRUNCATE TABLE users CASCADE;
        """))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_service(db: Session):
    try:
        db.execute(text("""
            TRUNCATE TABLE services CASCADE;
        """))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

# def show_users(db: Session):
#     try:
#         rows = db.execute(text("""
#             SELECT * FROM users;
#         """))
#         db.commit()
#         return rows
#     except Exception as e:
#         db.rollback()
#         raise e