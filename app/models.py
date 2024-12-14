from sqlalchemy import Column, Integer, String, ForeignKey, Float, Time, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String(15), nullable=False)
    role = Column(String, nullable=False)  # клиент/тренер


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False, unique=True)
    price_per_hour = Column(Integer, nullable=False)


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    trainer = relationship("User", foreign_keys=[trainer_id])
    service = relationship("Service", foreign_keys=[service_id])


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    total_cost = Column(Float, nullable=True)

    client = relationship("User", foreign_keys=[client_id])
    schedule = relationship("Schedule", foreign_keys=[schedule_id])
