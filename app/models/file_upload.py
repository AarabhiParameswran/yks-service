from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class FileUpload(Base):
    __tablename__ = "file_upload"

    id = Column(Integer, primary_key=True, index=True)
    upasabha_code = Column(String, index=True)
    file_url = Column(String)
    pic_number = Column(Integer)
    created_at = Column(DateTime,default=func.now(), server_default=func.now())
    created_by = Column(Integer,nullable=True) 
    updated_at = Column(DateTime, onupdate=func.now())
    updated_by = Column(Integer,nullable=True) 