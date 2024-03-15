from fastapi import Depends
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
import qrcode
from starlette.responses import StreamingResponse
import io

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def create_qr_codes(db: db_dependency) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url.target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_file_path = f"qr_codes/{url.key}.png"  # Adjust as needed
    img.save(qr_code_file_path)



















def generate(message: str):
    img = qrcode.make(message)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf.getvalue
    # return StreamingResponse(buf, media_type="image/jpeg")