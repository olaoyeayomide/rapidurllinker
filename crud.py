from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from models import ShortnedURL
from schemas import URLBase, URLConfig, URLInfo, QRCode
import keygen
import models
from qrcode import make as make_qr_code

import schemas
from app_config import get_settings
from yarl import URL
import qrcode
from starlette.responses import StreamingResponse
import io

url_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_db_url(db: db_dependency, url: URLBase) -> models.ShortnedURL:
    key = keygen.create_random_keys(length=4)
    secret_key = f"{key}_{keygen.create_random_keys(length=8)}"

    db_url = models.ShortnedURL(
        original_url=url.original_url, key=key, secret_key=secret_key
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url



def get_db_url_by_secret_key(db: db_dependency, secret_key: str) -> models.ShortnedURL:
    return (
        db.query(models.ShortnedURL)
        .filter(models.ShortnedURL.secret_key == secret_key, models.ShortnedURL.is_active)
        .first()
    )

def get_db_url_by_key(db: db_dependency, url_key: str) -> models.ShortnedURL:
    return (
        db.query(models.ShortnedURL)
        .filter(models.ShortnedURL.key == url_key, models.ShortnedURL.is_active)
        .first()
    )

# CLICK UPDATES
def update_db_clicks(db: db_dependency, db_url: schemas.URLConfig) -> models.ShortnedURL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_db_url_by_secret_key(
    db: db_dependency, secret_key: str
) -> models.ShortnedURL:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.delete(db_url)
        db.commit()
    return db_url

def deactivate_db_url_by_id(db: db_dependency, id: int):
    db_url = db.query(ShortnedURL).filter(ShortnedURL.id == id).first()
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
        return db_url
    return None


# QR CODE GENERATOR
def generate_qr_code_url(db: db_dependency, url: str, key: str, secret_key: str, ) -> ShortnedURL:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="purple", back_color="white")
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    qr_code_model = ShortnedURL(
        original_url=url,
        key=key,
        secret_key=secret_key,
        qr_code_image=img_io.getvalue()
    )
    db.add(qr_code_model)
    db.commit()
    db.refresh(qr_code_model)
    
    return qr_code_model
