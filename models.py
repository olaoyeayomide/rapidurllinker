from database import Base
from sqlalchemy import  Column, Integer, String, Boolean, Text, LargeBinary

class ShortnedURL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    original_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0) 
    qr_code_image = Column(LargeBinary, nullable=True)
    shortened_url= Column(String, index=True)
    admin_url= Column(String, index=True)


