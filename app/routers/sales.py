from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date
from app.views.sales import (
    compare_two_categories_revenue,
    get_sales_summary_view,
    compare_revenue_view,
    filter_sales_view,
)
from database import get_db
from app.schemas import StandardResponse, SaleOut
from typing import List, Dict

router = APIRouter()


@router.get("/summary", response_model=StandardResponse[List[Dict[str, float]]])
def sales_summary(
    interval: str = Query("daily", enum=["daily", "weekly", "monthly", "yearly"]),
    db: Session = Depends(get_db),
):
    return get_sales_summary_view(interval, db)


@router.get("/compare", response_model=StandardResponse[dict])
def compare_revenue(
    start1: date,
    end1: date,
    start2: date,
    end2: date,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return compare_revenue_view(start1, end1, start2, end2, category, db)


@router.get("/compare-category", response_model=StandardResponse[dict])
def compare_categories(category1: str, category2: str, db: Session = Depends(get_db)):
    return compare_two_categories_revenue(db, category1, category2)


@router.get("/filter", response_model=StandardResponse[list[SaleOut]])
def filter_sales(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return filter_sales_view(start_date, end_date, product_id, category, db)
