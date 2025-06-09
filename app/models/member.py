from sqlalchemy import Column, Integer, String, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Members(Base):
    __tablename__ = "yksyknmembers"

    member_id = Column(Float, primary_key=True, index=True)
    name = Column(String)
    house = Column(String)
    addr_1 = Column(String)
    addr_2 = Column(String)
    addr_3 = Column(String)
    district = Column(String)
    pincode = Column(Integer)
    phone = Column(String)
    mobile_number = Column(BigInteger)
    sex = Column(String)
    dob = Column(String)  
    age = Column(Integer)
    job = Column(String)
    member_type = Column(Integer)
    live = Column(String)
    upasabha_code = Column(Integer)
    district_code = Column(Integer)
    blood_group = Column(Integer)
    personal_id = Column(Integer)
    us_apd = Column(String)
    jilla_apd = Column(String)
    state_apd = Column(String)
    cro_apd = Column(String)
    locked = Column(String)
    ref_id = Column(Float)
    dc_year = Column(String)
    whatsapp_number = Column(String)
    email = Column(String)
    renewal = Column(String)
