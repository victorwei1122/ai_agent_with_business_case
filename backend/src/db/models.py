from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from src.db.database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    tier = Column(String, default="Bronze")
    joined = Column(String, nullable=False)

    orders = relationship("Order", back_populates="customer")
    tickets = relationship("SupportTicket", back_populates="customer")

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    description = Column(String)
    brand = Column(String)
    specs = Column(String) # JSON or descriptive string
    warranty = Column(String)
    tags = Column(String) # Comma-separated tags
    in_stock = Column(Boolean, default=True)
    
    reviews = relationship("ProductReview", back_populates="product")

class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String)
    customer_name = Column(String)
    date = Column(String)

    product = relationship("Product", back_populates="reviews")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    ordered_date = Column(String, nullable=False)
    shipped_date = Column(String, nullable=True)
    delivered_date = Column(String, nullable=True)
    cancelled_date = Column(String, nullable=True)
    returned_date = Column(String, nullable=True)
    tracking_number = Column(String, nullable=True)
    estimated_delivery = Column(String, nullable=True)
    cancel_reason = Column(String, nullable=True)
    refund_status = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=True)
    subject = Column(String, nullable=False)
    status = Column(String, default="open")
    priority = Column(String, default="normal")
    created = Column(String, nullable=False)
    resolved = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="tickets")
