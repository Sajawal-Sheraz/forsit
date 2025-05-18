# manage.py

from database import Base, engine

# from .insert_data import db


def seed_data():
    from sqlalchemy.orm import Session
    from database import SessionLocal
    from app.models import Product, Inventory, Sale
    from datetime import datetime, timedelta
    import random

    db: Session = SessionLocal()
    # Clear existing data
    db.query(Sale).delete()
    db.query(Inventory).delete()
    db.query(Product).delete()
    db.commit()

    # Sample products
    sample_products = [
        {"name": "Wireless Mouse", "category": "Electronics", "price": 29.99},
        {"name": "Bluetooth Keyboard", "category": "Electronics", "price": 49.99},
        {"name": "HD Monitor", "category": "Electronics", "price": 199.99},
        {"name": "Desk Lamp", "category": "Home", "price": 39.99},
        {"name": "Ergonomic Chair", "category": "Furniture", "price": 149.99},
        {"name": "Standing Desk", "category": "Furniture", "price": 299.99},
    ]

    products = []

    # Insert products and inventory
    for item in sample_products:
        product = Product(**item)
        db.add(product)
        db.flush()  # Get the product ID before commit
        inventory = Inventory(product_id=product.id, quantity=random.randint(5, 100))
        db.add(inventory)
        products.append(product)

    db.commit()

    # Insert random sales over the past 60 days
    today = datetime.utcnow()
    for _ in range(150):  # 150 sales entries
        product = random.choice(products)
        quantity = random.randint(1, 5)
        total_price = round(quantity * product.price, 2)
        days_ago = random.randint(0, 60)
        timestamp = today - timedelta(
            days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59)
        )
        sale = Sale(
            product_id=product.id,
            quantity=quantity,
            total_price=total_price,
            timestamp=timestamp,
        )
        db.add(sale)

    db.commit()
    db.close()

    print("✅ Database seeded with products, inventory, and sales data.")


def reset_and_seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_data()  # run seed script
    print("✅ Database reset and seeded.")


if __name__ == "__main__":
    reset_and_seed()
