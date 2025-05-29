from sqlalchemy import Column, Integer, String, Boolean, DateTime, text, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


# model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Double, nullable=False)
    user_name = Column(String(100), nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())

   