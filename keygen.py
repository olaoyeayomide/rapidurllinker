from fastapi import Depends
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session

import secrets
import string
import crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_random_keys(length: int = 4) -> str:
    chars = string.ascii_lowercase  + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: db_dependency) -> str:
    key = create_random_keys()
    while crud.get_db_url_by_key(db, key):
        key = create_random_keys()
    return key