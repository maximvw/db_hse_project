from sqlalchemy.orm import Session
from app.models import User, Service, Schedule, Booking
from sqlalchemy import text


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


def create_database():
    # Логика создания базы данных
    pass

def delete_database():
    # Логика удаления базы данных
    pass

def get_table_data(db, table_name):
    return db.execute(text(f"SELECT * FROM {table_name}")).fetchall()

def clear_table(db, table_name):
    db.execute(text(f"TRUNCATE TABLE {table_name}"))

def add_user(db, name, phone, role):
    db.execute(text("CALL add_user(:name, :phone, :role)"), {"name": name, "phone": phone, "role": role})

def search_by_field(db, table, field, value):
    return db.execute(text(f"SELECT * FROM {table} WHERE {field} = :value"), {"value": value}).fetchall()

def update_row(db, table, row_id, updates):
    set_clause = ", ".join([f"{key} = :{key}" for key in updates.keys()])
    db.execute(text(f"UPDATE {table} SET {set_clause} WHERE id = :id"), {"id": row_id, **updates})

def delete_by_field(db, table, field, value):
    db.execute(text(f"DELETE FROM {table} WHERE {field} = :value"), {"value": value})

def delete_by_id(db, table, row_id):
    db.execute(text(f"DELETE FROM {table} WHERE id = :id"), {"id": row_id})
