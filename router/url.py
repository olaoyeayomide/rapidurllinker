from fastapi import HTTPException, Depends, APIRouter,Request, Form
from typing import Annotated, List
from sqlalchemy.orm import Session
import validators
from schemas import URLBase, URLInfo, URLConfig, QRCode
import models, schemas, models
from starlette import status
from starlette.responses import StreamingResponse
from models import ShortnedURL
from database import engine, SessionLocal
from fastapi.responses import RedirectResponse, JSONResponse
import crud
from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL
from app_config import get_settings
from qrcode import make as make_qr_code 
from crud import  generate_qr_code_url
from fastapi.responses import HTMLResponse
import qrcode
import base64
import keygen

import io


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

# ERROR RESPONSE MESSAGE
def invalid_request(message):
    raise HTTPException(status_code=400, details=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)



@url_router.get("/home", response_class=HTMLResponse)
async def get_all_by(request:Request, db:db_dependency):
    url_home = db.query(ShortnedURL).filter(ShortnedURL.id == 1).all()

    return templates.TemplateResponse("home.html", {"request": request, "url_home": url_home})

@url_router.get("/add-url", response_class=HTMLResponse)
async def add_url_form(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request})

@url_router.get("/history", response_class=HTMLResponse)
async def get_history(request:Request, db:db_dependency):
    urls = db.query(ShortnedURL).all()
    return templates.TemplateResponse("history.html", {"request": request, "urls": urls})



@url_router.post("/generate_url_and_qr", response_model=schemas.URLInfo)
def generate_url_and_qr(db: db_dependency, url: URLBase) -> models.ShortnedURL:
    key = keygen.create_random_keys(length=4)
    secret_key = f"{key}_{keygen.create_random_keys(length=8)}"
    db_url = crud.generate_qr_code_url(db=db, url=url.original_url, key=key, secret_key=secret_key)

    db_url = get_admin_info(db=db, db_url=db_url)

    return db_url

@url_router.post("/add-url", response_model=schemas.URLInfo)
def create_url(request: Request, db: db_dependency, original_url: str = Form(...)):
    if not validators.url(original_url):
        raise HTTPException(status_code=400, detail="The provided URL is invalid.")
    
    db_url = generate_url_and_qr(db=db, url=schemas.URLBase(original_url=original_url))

    print(f"Generated shortened URL: {db_url.shortened_url}")
    print(f"Stored key in DB: {db_url.key}")

    return templates.TemplateResponse("home.html", {
    "request": request,
    "shortened_url": db_url.shortened_url,
    "original_url": original_url,
    "qr_code_image": base64.b64encode(db_url.qr_code_image).decode('utf-8')

})


def get_admin_info(db: db_dependency, db_url: schemas.URLInfo) -> models.ShortnedURL:
    base_url = URL(get_settings().base_url)
    admin_endpoint = url_router.url_path_for(
        "admin info", secret_key=db_url.secret_key
    )
    # Use the new base URL, which is "http://rli"
    db_url.shortened_url = str(base_url.replace(path=f"rapid_linker/{db_url.key}"))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

# GET ALL URLs
@url_router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency):
     all_urls = db.query(models.ShortnedURL).all()
     return all_urls

# Get A URL
@url_router.get("/url/{url_id}", status_code=status.HTTP_200_OK)
async def get_one(db: db_dependency, url_id: int):
    url = db.query(models.ShortnedURL).filter(models.ShortnedURL.id == url_id).first()
    if url is None:
        raise HTTPException(status_code=404,
                            detail="URL not found")
    return url


@url_router.get("/{url_key}")
def forward_to_original_url(
    url_key: str,
    request: Request,
    db: db_dependency
    ):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.original_url, status_code=302)
    else:
        raise_not_found(request)



# ORIGINAL
@url_router.get("/admin/{secret_key}", name="admin info", response_model=schemas.URLInfo,)

def get_url_info(secret_key: str, request: Request, db: db_dependency):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db, db_url)
    else:
        raise_not_found(request)


# DELETE
@url_router.delete("/delete/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: db_dependency):
    
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = (
            f"Successfully deleted shortened URL for '{db_url.original_url}'"
        )
        return {"detail": message}
    else:
        raise_not_found(request)







# ORIGINAL ROUTERS
# CREATE URL
# @url_router.pgenerate_url_and_qr", response_model=schemas.URLInfo)
# async def create_url(request: Request, db: db_dependency, original_url: str = Form(...)):
#     if not validators.url(original_url):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided URL is invalid.")
    
#     # Create the shortened URL
#     url = URLBase(original_url=original_url)
#     db_url = crud.create_db_url(db=db, url=url)

#     db_url_info = get_admin_info(db, db_url)

#     # Generate the QR code for the shortened URL
#     qr_code_model = crud.generate_qr_code_url(db_url_info.shortened_url, db)
    
#     # Convert QR code to a format suitable for HTML
#     img_io = io.BytesIO(qr_code_model.qr_code_image)
#     img_io.seek(0)
#     qr_code_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

#     # Return the template response including the shortened URL and QR code
#     return templates.TemplateResponse("home.html", {
#         "request": request,
#         "shortened_url": db_url_info.shortened_url,
#         "original_url": original_url,
#         "qr_code_base64": qr_code_base64
#     })

# @url_router.post("/url", response_model=schemas.URLInfo)
# # Add this later , response_model=schemas.URLInfo
# def create_url(url: URLBase, db: db_dependency):
#     if not validators.url(url.original_url):
#         invalid_request(message="Your provided URL is invalid")

#     db_url = crud.create_db_url(db=db, url=url)

#     qr_code_file_path = f"qr_codes/{db_url.id}.png"
#     generate_qr_code(db_url.original_url, qr_code_file_path)
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
