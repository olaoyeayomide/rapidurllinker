from fastapi import Depends
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
import qrcode
from starlette.responses import StreamingResponse
import io
from schemas import URLBase

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# def create_qr_codes(url: URLBase):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url.target_url)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
#     qr_code_file_path = f"qr_codes/{url.key}.png"
#     img.save(qr_code_file_path)


# url = ("https://example.com", "example_key")
# create_qr_codes(url)

# def create_qr_codes(url: URLBase):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url.target_url)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
#     qr_code_file_path = f"qr_codes/{url.key}.png"
#     img.save(qr_code_file_path)


# url = ("https://example.com", "example_key")
# create_qr_codes(url)



def generate_qr_code(url: URLBase, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="green", back_color="white")
    img.save(file_path)

# Example usage:
url = "https://app.bitly.com/Bo2d8F1iImy/home"
file_path = "qrcode.png"
generate_qr_code(url, file_path)
