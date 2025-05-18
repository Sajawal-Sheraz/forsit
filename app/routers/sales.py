from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import Sale
from app.schemas import SaleOut
from database import get_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[SaleOut])
def get_sales(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db),
):
    return (
        db.query(Sale)
        .filter(Sale.timestamp >= start_date, Sale.timestamp <= end_date)
        .all()
    )


@router.get("/revenue")
def get_revenue_summary(
    period: str = Query("daily", enum=["daily", "weekly", "monthly", "yearly"]),
    db: Session = Depends(get_db),
):
    interval_map = {
        "daily": func.date(Sale.timestamp),
        "weekly": func.yearweek(Sale.timestamp),
        "monthly": func.date_format(Sale.timestamp, "%Y-%m"),
        "yearly": func.year(Sale.timestamp),
    }
    group_by_expr = interval_map.get(period)

    data = (
        db.query(
            group_by_expr.label("period"), func.sum(Sale.total_price).label("revenue")
        )
        .group_by(group_by_expr)
        .order_by(group_by_expr)
        .all()
    )
    return data
