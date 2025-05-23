# generics.py or schemas.py
from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Optional, List
from datetime import datetime

T = TypeVar("T")


class StandardResponse(GenericModel, Generic[T]):
    status: str
    message: str
    result: Optional[T] = None


class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    created_at: datetime

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    category: str
    price: float


class PaginatedResponse(GenericModel, Generic[T]):
    products: List[T]
    total: int
    page: int
    size: int


class InventoryOut(BaseModel):
    product_id: int
    quantity: int
    updated_at: datetime

    class Config:
        orm_mode = True


class SaleOut(BaseModel):
    id: int
    quantity: int
    total_price: float
    timestamp: datetime
    product: ProductOut

    class Config:
        orm_mode = True


class InventoryUpdate(BaseModel):
    product_id: int
    quantity: int
