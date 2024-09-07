from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app_config import get_settings

engine = create_engine(
    get_settings().db_url)

SessionLocal = sessionmaker(
    autoflush=False, bind=engine, autocommit=False
)
Base = declarative_base()
