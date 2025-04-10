from sqlalchemy.orm import Session
from datetime import timedelta, timezone
from fastapi import HTTPException
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate


def get_reservations(db: Session):
    """Return all reservations from the database."""
    return db.query(Reservation).all()


def create_reservation(db: Session, reservation_data: ReservationCreate):
    """
    Create a new reservation if the table is available.

    Checks the requested time slot (from reservation_time to reservation_time + duration_minutes)
    against all existing reservations for the same table.

    Raises:
        HTTPException: 400 error if the new reservation overlaps with an existing reservation.
    """
    # Retrieve new reservation start and compute end time
    new_start = reservation_data.reservation_time
    new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

    # Normalize new reservation datetimes to UTC naive (no tzinfo)
    if new_start.tzinfo is not None:
        new_start = new_start.astimezone(timezone.utc).replace(tzinfo=None)
    if new_end.tzinfo is not None:
        new_end = new_end.astimezone(timezone.utc).replace(tzinfo=None)

    # Fetch existing reservations for the specified table
    existing_reservations = db.query(Reservation).filter(
        Reservation.table_id == reservation_data.table_id
    ).all()

    # Check each existing reservation for overlapping intervals
    for reservation in existing_reservations:
        existing_start = reservation.reservation_time
        existing_end = existing_start + timedelta(minutes=reservation.duration_minutes)

        # Normalize existing reservation datetimes to UTC naive as well
        if existing_start.tzinfo is not None:
            existing_start = existing_start.astimezone(timezone.utc).replace(tzinfo=None)
        if existing_end.tzinfo is not None:
            existing_end = existing_end.astimezone(timezone.utc).replace(tzinfo=None)

        # Overlap check: new reservation intersects the existing one if both conditions are met
        if new_start < existing_end and existing_start < new_end:
            raise HTTPException(
                status_code=400,
                detail="Table is already booked for the specified time slot."
            )

    # Create and commit the new reservation if no conflicts are found
    new_reservation = Reservation(**reservation_data.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


def delete_reservation(db: Session, reservation_id: int):
    """Delete a reservation by its ID."""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
        return True
    return False
