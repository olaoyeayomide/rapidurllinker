from pydantic import BaseModel

class URLBase(BaseModel):
    original_url: str

class URLConfig(URLBase):
    id: int
    is_active: bool
    clicks: int

    class Config:
        from_attributes = True

class URLInfo(URLConfig):
    shortened_url: str
    admin_url: str

class QRCode(URLBase):
    image: str