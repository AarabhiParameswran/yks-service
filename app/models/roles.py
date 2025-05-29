from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


# model
class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(100), nullable=False)
    created_at = Column(DateTime,default=func.now(), server_default=func.now())
    created_by = Column(Integer,nullable=True) 
   