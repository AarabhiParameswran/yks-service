from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# model
class Upasabha(Base):
    __tablename__ = "upasabha"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district_code = Column(Integer, nullable=False)
    upasabha_code = Column(Integer, nullable=False)
    upasabha_name = Column(String(100), nullable=False)
    editable = Column(String(100), nullable=False)
    # created_at = Column(DateTime, server_default=text('CURRENT_DateTime'))
    # created_by = Column(Integer,nullable=True) 
   