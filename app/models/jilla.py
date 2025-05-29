from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# model
class Jilla(Base):
    __tablename__ = "jilla"

    district_code = Column(Integer, primary_key=True, autoincrement=True)
    district_name = Column(String(100), nullable=False)

   