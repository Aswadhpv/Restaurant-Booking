from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.table import TableCreate, TableRead
from app.services.table_service import get_tables, create_table, delete_table
from app.database import get_db

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/", response_model=list[TableRead])
def read_tables(db: Session = Depends(get_db)):
    return get_tables(db)

@router.post("/", response_model=TableRead)
def create_new_table(table: TableCreate, db: Session = Depends(get_db)):
    return create_table(db, table)

@router.delete("/{table_id}")
def remove_table(table_id: int, db: Session = Depends(get_db)):
    if not delete_table(db, table_id):
        raise HTTPException(status_code=404, detail="Table not found")
    return {"detail": "Table deleted successfully"}
