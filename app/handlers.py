from datetime import date, time

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import User, Service, Schedule, Booking


def add_user(db: Session, name: str, phone: str, role: str):
    try:
        # new_user = User(name=name, phone=phone, role=role)
        # db.add(new_user)

        db.execute(text("CALL add_user(:p1, :p2, :p3)"), {"p1": name, "p2": phone, "p3": role})

        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_service(db: Session, name: str, price: str):
    try:
        new_service = Service(service_name=name, price_per_hour=int(price))
        db.add(new_service)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_schedule(db: Session, trainer_id: int, service_id: int, date_: date, start_time: time, end_time: time):
    try:
        new_schedule = Schedule(trainer_id=trainer_id, service_id=service_id, date=date_, start_time=start_time,
                                end_time=end_time)
        db.add(new_schedule)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def add_booking(db: Session, client_id: str, schedule_id: str, total_cost: str = None):
    try:
        new_booking = Booking(client_id=int(client_id), schedule_id=int(schedule_id), total_cost=0)
        db.add(new_booking)
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
    except Exception as e:
        db.rollback()
        raise e


def clear_schedule(db: Session):
    try:
        db.query(Schedule).delete()
    except Exception as e:
        db.rollback()
        raise e


def clear_user(db: Session):
    try:
        db.query(User).delete()
    except Exception as e:
        db.rollback()
        raise e


def clear_service(db: Session):
    try:
        db.query(Service).delete()
    except Exception as e:
        db.rollback()
        raise e
