from database import Base
from sqlalchemy import  Column, Integer, String, Boolean

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0) 
    qr_code_image = Column(String)



    
    # original_url = Column(String, index=True)
    # shortened_url = Column(String, unique=True, index=True)



