from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from datetime import timedelta

def get_reservations(db: Session):
    return db.query(Reservation).all()

def create_reservation(db: Session, reservation_data: ReservationCreate):
    new_start = reservation_data.reservation_time
    new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

    # Check for time conflict for the same table.
    existing_reservations = db.query(Reservation).filter(Reservation.table_id == reservation_data.table_id).all()
    for res in existing_reservations:
        existing_start = res.reservation_time
        existing_end = existing_start + timedelta(minutes=res.duration_minutes)
        if new_start < existing_end and existing_start < new_end:
            raise Exception("Table is already booked for the specified time slot.")

    reservation = Reservation(**reservation_data.dict())
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
        return True
    return False
