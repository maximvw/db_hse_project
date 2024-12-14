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
        db.execute(text("CALL add_service(:trainer_id, :service_id, :date_calendar, :start_time, :end_time)"),
                   {"trainer_id": trainer_id, "service_id": service_id, "date_calendar": date_calendar,
                    "start_time": start_time, "end_time": end_time})
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_booking(db: Session, client_id: str, schedule_id: str, total_cost: float = 0):
    try:
        db.execute(text("CALL add_service(:client_id, :schedule_id, :total_cost)"),
                   {"client_id": client_id, "schedule_id": schedule_id, "total_cost": total_cost})
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def get_users(db: Session):
    return db.query(User).all()


def clear_tables(db: Session):
    try:
        db.query(Booking).delete()
        db.query(Schedule).delete()
        db.query(User).delete()
        db.query(Service).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_booking(db: Session):
    try:
        db.query(Booking).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_schedule(db: Session):
    try:
        db.query(Schedule).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_user(db: Session):
    try:
        db.query(User).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def clear_service(db: Session):
    try:
        db.query(Service).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
