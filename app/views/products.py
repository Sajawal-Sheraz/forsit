from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import PaginatedResponse, StandardResponse, ProductOut
from app.utils.response import standard_response
from app.models import Product as ProductORM


def get_products_view(request, db):
    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 10))
    offset = (page - 1) * size
    query = db.query(Product)
    total = query.count()
    products = query.offset(offset).limit(size).all()
    paginated = PaginatedResponse(
        products=products,
        total=total,
        page=page,
        size=size,
    )
    return standard_response(
        data=paginated, message="Products retrieved successfully", status="success"
    )


def create_product_view(request, db):
    new_product = Product(
        name=request.name, category=request.category, price=request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
