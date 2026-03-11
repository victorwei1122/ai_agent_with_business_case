from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Read from environment strictly for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

# Create the SQLAlchemy engine for Postgres
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
