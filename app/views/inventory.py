from sqlalchemy.orm import Session
from app.schemas import StandardResponse, InventoryOut
from fastapi import HTTPException
from app.models import Inventory, Product


def get_inventory_status_view(db: Session, low_stock_threshold: int = None):
    query = db.query(Inventory)

    if low_stock_threshold is not None:
        query = query.filter(Inventory.quantity < low_stock_threshold)

    inventory = query.all()
    results = [
        InventoryOut(
            product_id=i.product_id, quantity=i.quantity, updated_at=i.updated_at
        )
        for i in inventory
    ]

    message = (
        f"Low stock items (threshold < {low_stock_threshold})"
        if low_stock_threshold is not None
        else "All inventory items"
    )

    return StandardResponse(status="success", message=message, result=results)


def update_inventory_view(data, db: Session):
    inventory = (
        db.query(Inventory).filter(Inventory.product_id == data.product_id).first()
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory.quantity = data.quantity
    db.commit()
    db.refresh(inventory)
    return StandardResponse(
        status="success", message="Inventory updated", result=inventory
    )
