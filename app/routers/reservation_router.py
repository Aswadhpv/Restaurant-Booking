from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services.reservation_service import get_reservations, create_reservation, delete_reservation
from app.database import get_db

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("/", response_model=list[ReservationRead])
def read_reservations(db: Session = Depends(get_db)):
    return get_reservations(db)

@router.post("/", response_model=ReservationRead)
def create_new_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return create_reservation(db, reservation)
    except HTTPException as he:
        # Re-raise the HTTPException unchanged so that the detail message remains intact.
        raise he
    except Exception as e:
        # Wrap any other exception in an HTTPException
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{reservation_id}")
def remove_reservation(reservation_id: int, db: Session = Depends(get_db)):
    if not delete_reservation(db, reservation_id):
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"detail": "Reservation deleted successfully"}
