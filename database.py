from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app_config import get_settings

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./shortener database.db'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autoflush=False, bind=engine, autocommit=False
)
Base = declarative_base()
