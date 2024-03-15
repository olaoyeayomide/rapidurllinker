from fastapi import HTTPException, Depends, APIRouter,Request
from typing import Annotated, List
from sqlalchemy.orm import Session
import validators
from schemas import URLBase, URLInfo, QRCode
import models, schemas, models
from starlette import status
from models import URL
from database import engine, SessionLocal
from fastapi.responses import RedirectResponse
import crud
from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL
from app_config import get_settings
from qrcode import make as make_qr_code
from crud import create_qr_code
import qrcode



url_router = APIRouter()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def invalid_request(message):
    raise HTTPException(status_code=400, details=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = url_router.url_path_for(
        "admin info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

@url_router.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# GET ALL URLs
@url_router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency):
     all_urls = db.query(models.URL).all()
     return all_urls

# Get A URL
@url_router.get("/url/{url}", status_code=status.HTTP_200_OK)
async def get_one(db: db_dependency, url_id: int):
    url = db.query(models.URL).filter(models.URL.id == url_id).first()
    if url is None:
        raise HTTPException(status_code=404,
                            detail="Authentication Failed")
    return url


@url_router.post("/url", response_model=schemas.URLInfo)
def create_url(url: URLBase, db: db_dependency):
    if not validators.url(url.target_url):
        invalid_request(message="Your provided URL is invalid")
    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@url_router.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: db_dependency
    ):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)



@url_router.get("/admin/{secret_key}", name="admin info", response_model=schemas.URLInfo,)

def get_url_info(secret_key: str, request: Request, db: db_dependency):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)




@url_router.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: db_dependency):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shorthand URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)



# Generate QR CODE
@url_router.post("/generate_qr_code/", response_model=QRCode)
async def generate_qr_code(qr_code: QRCode, db: db_dependency):
    return create_qr_code(db, qr_code)





















# @url_router.post("/generate_qr_code/")
# async def generate_qr_code(url: URLBase, db: db_dependency):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url.target_url)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")
#     qr_code_file_path = f"qr_codes/{url.key}.png"  # Adjust as needed
#     img.save(qr_code_file_path)

#     # Save the URL and QR code file path to the database
#     db_url = crud_db_url(db=db, url=url)
#     db_url.qr_code_path = qr_code_file_path
#     db.commit()

    # return {"message": "QR code generated successfully"}
    return get_admin_info(db_url)












































# @url_router.post("/url", response_model=schemas.URLInfo)
# # Add this later , response_model=schemas.URLInfo
# def create_url(url: URLBase, db: db_dependency):
#     if not validators.url(url.target_url):
#         invalid_request(message="Your provided URL is invalid")

#     db_url = crud.create_db_url(db=db, url=url)

#     qr_code_file_path = f"qr_codes/{db_url.id}.png"
#     generate_qr_code(db_url.target_url, qr_code_file_path)
#     db_url.qr_code_path = qr_code_file_path
#     db.commit()

#     return db_url
    
#     # return get_admin_info(db_url)

# def raise_not_found(request):
#     message = f"URL '{request.url}' doesn't exist"
#     raise HTTPException(status_code=404, detail=message)


# @url_router.get("/qr_code/{url_key}/")
# async def get_qr_code(url_key: str, db: Session = Depends(get_db)):
#     db_url = crud.get_db_url_by_key(db=db, url_key=url_key)
#     if not db_url:
#         raise HTTPException(status_code=404, detail="URL not found")
    
#     if not db_url.qr_code_path:
#         raise HTTPException(status_code=404, detail="QR code not found")

#     return FileResponse(db_url.qr_code_path)
