from sqlalchemy.orm import Session
from app.models import User, Service, Schedule, Booking


def add_user(db: Session, name: str, phone: str, role: str):
    new_user = User(name=name, phone=phone, role=role)
    db.add(new_user)
    db.commit()


def get_users(db: Session):
    return db.query(User).all()


def clear_tables(db: Session):
    db.query(Booking).delete()
    db.query(Schedule).delete()
    db.query(User).delete()
    db.commit()
