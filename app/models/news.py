from sqlalchemy import Column, Integer, String, Boolean, DateTime, text,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer,nullable = True)
    category = Column(String(45),nullable = False)
    news = Column(String(500),nullable = False)
    created_at = Column(DateTime,default=func.now(), server_default=func.now())
    created_by = Column(Integer,nullable=True) 
    updated_at = Column(DateTime, onupdate=func.now())
    updated_by = Column(Integer,nullable=True) 