from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ProductCreate, ProductOut
from app.views.products import get_products_view, create_product_view
from app.schemas import PaginatedResponse, StandardResponse
from typing import List
from database import get_db
from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request

router = APIRouter()


# retrieve products
@router.get("/", response_model=StandardResponse[PaginatedResponse[ProductOut]])
def get_products_api(request: Request, db: Session = Depends(get_db)):
    return get_products_view(request, db)


# create product
@router.post("/create", response_model=ProductOut)
def create_product_api(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_view(product, db)
