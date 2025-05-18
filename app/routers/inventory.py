from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.views.inventory import get_inventory_status_view, update_inventory_view
from database import get_db
from app.schemas import InventoryOut, InventoryUpdate, StandardResponse
from pydantic import BaseModel

router = APIRouter()


@router.get("/", response_model=StandardResponse[list[InventoryOut]])
def get_inventory_status(threshold: int = None, db: Session = Depends(get_db)):
    return get_inventory_status_view(db, low_stock_threshold=threshold)


@router.post("/update", response_model=StandardResponse[InventoryOut])
def update_inventory(data: InventoryUpdate, db: Session = Depends(get_db)):
    return update_inventory_view(data, db)
