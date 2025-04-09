from sqlalchemy.orm import Session
from app.models.table import Table
from app.schemas.table import TableCreate

def get_tables(db: Session):
    return db.query(Table).all()

def create_table(db: Session, table_data: TableCreate):
    table = Table(**table_data.dict())
    db.add(table)
    db.commit()
    db.refresh(table)
    return table

def delete_table(db: Session, table_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    if table:
        db.delete(table)
        db.commit()
        return True
    return False
