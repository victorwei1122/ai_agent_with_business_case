from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Read from environment strictly for PostgreSQL, fallback to sqlite for local dev/testing
# Find database path in common locations
def get_db_path():
    paths = ["ecommerce.db", "backend/ecommerce.db", "../ecommerce.db"]
    for p in paths:
        if os.path.exists(p):
            return f"sqlite:///{os.path.abspath(p)}"
    return "sqlite:///./ecommerce.db"

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", get_db_path())

# Create the SQLAlchemy engine
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a scoped session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative ORM models
Base = declarative_base()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
