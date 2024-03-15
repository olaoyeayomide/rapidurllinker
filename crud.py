from fastapi import Depends, HTTPException
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from models import URL
from schemas import URLBase, URL, QRCode
import keygen
import models
from qrcode import make as make_qr_code
import qr_codegen

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_db_url(db: db_dependency, url: URLBase) -> models.URL:
    key = keygen.create_random_keys(length=4)
    secret_key = f"{key}_{keygen.create_random_keys(length=8)}"

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url

def get_db_url_by_key(db: db_dependency, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

def get_db_url_by_secret_key(db: db_dependency, secret_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )

def update_db_clicks(db: db_dependency, db_url: URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url



# def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
#     db_url = get_db_url_by_key(db, secret_key)
#     if db_url:
#         db_url.is_active = False
#         db.commit()
#         db.refresh(db_url)
#     return db_url





# def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
#         db_url = get_db_url_by_key(db, secret_key)
#         if db_url is None:
#             raise HTTPException(status_code=404, detail="Not Found")

#         db.delete(db_url)
#         db.commit()
#         db.refresh(db_url)



def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    db_url = get_db_url_by_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url





# QR CODE GENERATOR
def create_qr_code(db: Session, qr_code: QRCode) -> models.URL:
    qr_image = qr_codegen.generate(qr_code.message)

    db_qr_code = QRCode(message=qr_code.message, image=qr_image)
    db.add(db_qr_code)
    db.commit()
    db.refresh(db_qr_code)

    return db_qr_code























# def crud_db_url(db: Session, url: str, qr_code_path: str) -> models.URL:
#     """
#     Create a new URL entry in the database.

#     Parameters:
#     - db (Session): SQLAlchemy database session
#     - url (str): The URL to be stored in the database
#     - qr_code_path (str): The file path of the generated QR code

#     Returns:
#     - URL: The created URL object
#     """
#     # Perform database operation to create a new URL entry
#     db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key, qr_code_path=qr_code_path)
#     db.add(db_url)
#     db.commit()
#     db.refresh(db_url)
#     return db_url






























# def create_shortened_url(db: Session, original_url: str):
#     # Create the shortened URL
#     shortened_url = generate_shortened_url(original_url)

#     # Generate and save the QR code image
#     qr_code_image_path = f"qr_codes/{shortened_url}.png"
#     make_qr_code(original_url).save(qr_code_image_path)

#     # Save the shortened URL and its QR code image path to the database
#     db_url = models.URL(original_url=original_url, shortened_url=shortened_url, qr_code_image=qr_code_image_path)
#     db.add(db_url)
#     db.commit()
#     db.refresh(db_url)
#     return db_url



