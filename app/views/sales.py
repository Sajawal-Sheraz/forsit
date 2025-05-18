from sqlalchemy.orm import Session
from app.models import Sale, Product
from sqlalchemy import func, extract
from datetime import date
from app.schemas import StandardResponse

from datetime import datetime, time


def get_sales_summary_view(interval: str, db: Session):
    group_by_map = {
        "daily": func.date(Sale.timestamp),
        "weekly": extract("week", Sale.timestamp),
        "monthly": extract("month", Sale.timestamp),
        "yearly": extract("year", Sale.timestamp),
    }

    group = group_by_map.get(interval, func.date(Sale.timestamp))

    sales = (
        db.query(group.label("period"), func.sum(Sale.total_price).label("revenue"))
        .group_by(group)
        .all()
    )

    return StandardResponse(
        status="success",
        message="Sales summary",
        result=[{"period": str(s[0]), "revenue": s[1]} for s in sales],
    )


def compare_revenue_view(start1, end1, start2, end2, category, db: Session):
    def get_revenue(start, end):
        q = db.query(func.sum(Sale.total_price)).join(Product)
        q = q.filter(Sale.timestamp.between(start, end))
        if category:
            q = q.filter(Product.category == category)
        return q.scalar() or 0

    rev1 = get_revenue(start1, end1)
    rev2 = get_revenue(start2, end2)
    diff = rev2 - rev1

    return StandardResponse(
        status="success",
        message="Revenue comparison",
        result={
            "period_1": rev1,
            "period_2": rev2,
            "difference": diff,
        },
    )


def compare_two_categories_revenue(db: Session, category1: str, category2: str):
    query = (
        db.query(Product.category, func.sum(Sale.total_price).label("revenue"))
        .join(Sale.product)
        .filter(Product.category.in_([category1, category2]))
        .group_by(Product.category)
    )

    results = {r[0]: r[1] for r in query.all()}
    rev1 = results.get(category1, 0)
    rev2 = results.get(category2, 0)
    diff = rev2 - rev1

    return StandardResponse(
        status="success",
        message=f"Revenue comparison between {category1} and {category2}",
        result={
            "category1": {"name": category1, "revenue": rev1},
            "category2": {"name": category2, "revenue": rev2},
            "difference": diff,
        },
    )


def filter_sales_view(start_date, end_date, product_id, category, db: Session):
    q = db.query(Sale).join(Product)

    if start_date:
        start_datetime = datetime.combine(start_date, time.min)  # 00:00:00
        q = q.filter(Sale.timestamp >= start_datetime)

    if end_date:
        end_datetime = datetime.combine(end_date, time.max)  # 23:59:59.999999
        q = q.filter(Sale.timestamp <= end_datetime)

    if product_id:
        q = q.filter(Sale.product_id == product_id)

    if category:
        q = q.filter(Product.category == category)

    sales_list = q.all()

    return StandardResponse(
        status="success", message="Filtered sales", result=sales_list
    )
