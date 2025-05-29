import re
from app.database import get_db
from app.models.users import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
INVALID_DATE_MESSAGE = "Invalid date. Use 'YYYY-MM-DD' format."

class ValidationService:
    def __init__(self, db):
        self.db = db
    
    @staticmethod
    def check_email_validity(email):
        email_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]*[a-zA-Z0-9])?@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise HTTPException(status_code=422, detail="Please enter a valid email address.")
         
    @staticmethod
    def check_mobile_validity(mobile):
        if not (mobile.isdigit() and len(mobile) == 10):
            raise HTTPException(status_code=422, detail="Please enter a valid 10 digit mobile number")
        if mobile[0] == '0':
            raise HTTPException(status_code=422, detail="Mobile number cannot start with 0")
        if all(digit == mobile[0] for digit in mobile):
            raise HTTPException(status_code=422, detail="Mobile number cannot consist of all the same digit")
       
    def check_mobile_exits(self,mobile:str):
        check = self.db.query(User).filter(User.mobile_number == mobile).first()
        if check:
            raise HTTPException(status_code=400, detail="This mobile number already exists") 
        

    def check_email_exits(self,email_id:str):
        check = self.db.query(User).filter(User.email == email_id).first()
        if check:
            raise HTTPException(status_code=400, detail="This email already exists") 
        

def get_validation_service(
        db: Session = Depends(get_db)) -> ValidationService:
    return ValidationService(db)