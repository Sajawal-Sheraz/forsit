from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Inventory, Product
from app.schemas import InventoryOut
from database import get_db
from typing import Optional, List

router = APIRouter()


@router.get("/", response_model=List[InventoryOut])
def get_inventory_status(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@router.get("/low-stock", response_model=List[InventoryOut])
def get_low_stock_alerts(threshold: int = 10, db: Session = Depends(get_db)):
    return db.query(Inventory).filter(Inventory.quantity < threshold).all()
