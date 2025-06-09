from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class FamilyRelation(Base):
    __tablename__ = "family_relation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Float, nullable=False)
    family_member_id = Column(Float, nullable=False)
    relation = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(Integer, nullable=True)
