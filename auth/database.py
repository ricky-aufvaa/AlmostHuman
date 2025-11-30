from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from auth.models import Base
import os

# Database configuration
DATABASE_URL = "sqlite:///./auth.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
