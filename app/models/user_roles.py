from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


# model
class UserRoles(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), nullable=False)
    role_id = Column(String(100), nullable=False)
    created_at = Column(DateTime,default=func.now(), server_default=func.now())
    created_by = Column(Integer,nullable=True) 

   