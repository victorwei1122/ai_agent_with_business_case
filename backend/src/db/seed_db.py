from src.db.database import SessionLocal, engine, Base
from src.db.models import Customer, Product, Order, OrderItem, SupportTicket, ProductReview
from src.mock_data import CUSTOMERS, PRODUCTS, ORDERS, SUPPORT_TICKETS, PRODUCT_REVIEWS

def seed_database():
    # Only create tables if they don't exist, don't drop them every time
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if we already have data to avoid redundant work
        product_count = db.query(Product).count()
        if product_count > 0:
            print(f"Database already contains {product_count} products. Skipping seeding.")
            return

        print("Start seeding database...")
        for pid, pdata in PRODUCTS.items():
            product = Product(
                id=pid,
                name=pdata["name"],
                brand=pdata.get("brand"),
                category=pdata["category"],
                price=pdata["price"],
                rating=pdata["rating"],
                description=pdata["description"],
                specs=pdata.get("specs"),
                warranty=pdata.get("warranty"),
                tags=pdata.get("tags"),
                in_stock=pdata["in_stock"]
            )
            db.add(product)
        
        # 2. Seed Customers
        for cid, cdata in CUSTOMERS.items():
            customer = Customer(
                id=cid,
                name=cdata["name"],
                email=cdata["email"],
                tier=cdata["tier"],
                joined=cdata["joined"]
            )
            db.add(customer)
            
        db.flush() # Ensure products and customers are in session
        
        # 3. Seed Orders and Items
        for oid, odata in ORDERS.items():
            order = Order(
                id=oid,
                customer_id=odata["customer_id"],
                status=odata["status"],
                ordered_date=odata["ordered_date"],
                total=odata["total"],
                shipped_date=odata.get("shipped_date"),
                delivered_date=odata.get("delivered_date"),
                returned_date=odata.get("returned_date"),
                cancelled_date=odata.get("cancelled_date"),
                tracking_number=odata.get("tracking_number"),
                estimated_delivery=odata.get("estimated_delivery"),
                refund_status=odata.get("refund_status"),
                cancel_reason=odata.get("cancel_reason")
            )
            db.add(order)
            
            for item_data in odata["items"]:
                item = OrderItem(
                    order_id=oid,
                    product_id=item_data["product_id"],
                    qty=item_data["qty"],
                    price=item_data["price"]
                )
                db.add(item)
                
        # 4. Seed Support Tickets
        for tid, tdata in SUPPORT_TICKETS.items():
            ticket = SupportTicket(
                id=tid,
                customer_id=tdata["customer_id"],
                order_id=tdata["order_id"],
                subject=tdata["subject"],
                status=tdata["status"],
                priority=tdata["priority"],
                created=tdata["created"],
                resolved=tdata.get("resolved")
            )
            db.add(ticket)
            
        # 5. Seed Product Reviews
        for rdata in PRODUCT_REVIEWS:
            review = ProductReview(
                product_id=rdata["product_id"],
                rating=rdata["rating"],
                comment=rdata["comment"],
                customer_name=rdata["customer_name"],
                date=rdata["date"]
            )
            db.add(review)
            
        db.commit()
        print("Database seeded completely with high-quality mock data!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
