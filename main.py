from fastapi import FastAPI
from app.routers import sales, inventory, products
from database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Admin API")

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
