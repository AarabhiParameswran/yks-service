import asyncio
import secrets

import requests
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, requests
from app.database import get_db

OTP_EXPIRY_MINUTES = 5
NO_OF_DIGITS = 6
USER_NOT_FOUND_ERROR = "User not found"


class OTPService:

    def __init__(self, db: Session,
                # communication_service: CommunicationService
                ):
        self.db = db
        # self.communication_service=communication_service

    @staticmethod
    def generate_otp() -> str:
        return str(secrets.randbelow(10 ** NO_OF_DIGITS)).zfill(NO_OF_DIGITS)


    # def process_otp(self, otp_type: str, user) -> OTPResponse:
    #     otp = self.generate_otp()
    #     expiry_time = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    #     new_otp = OTPCode(
    #         user_id=user.id,
    #         otp_code=otp,
    #         otp_type=otp_type,
    #         created_at=datetime.now(),
    #         expires_at=expiry_time,
    #         is_used=False
    #     )

    #     self.db.add(new_otp)
    #     self.db.commit()
    #     if otp_type == "Email":
    #         email = user.email 
    #         user_name = user.first_name
    #         self.communication_service._send_sms_via_email(email,user_name,otp)
        
    #     if otp_type == "Mobile":            
    #         mobile_number = user.mobile_number 
    #         user_name = user.first_name
    #         self.communication_service._send_sms_via_msg91(mobile_number,user_name,otp)
            
    #     return OTPResponse(
    #         message=f"OTP sent successfully to {otp_type}",
    #         userId=user.id)


    # def verify_otp(self, otp_type: str, user: UserCreate, otp_code: str) -> OTPResponse:
    #     self.check_otp_validity(otp_code)
    #     otp_record = self.db.query(OTPCode).filter(
    #         and_(
    #             OTPCode.user_id == user.id,
    #             OTPCode.otp_type == otp_type,
    #             OTPCode.otp_code == otp_code,
    #             OTPCode.is_used == False,
    #             OTPCode.expires_at > datetime.now()
    #         )
    #     ).first()
    #     if not otp_record:
    #         raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    #     otp_record.is_used = True
    #     otp_record.updated_at = datetime.now()

    #     if otp_type == "Mobile":
    #         user.is_mobile_verified = True
    #         self.invalidate_unused_otp("Mobile",User.id)
    #     elif otp_type == "Email":
    #         user.is_email_verified = True
    #         self.invalidate_unused_otp("Email",User.id)
        
    #     self.db.commit()
    #     return OTPResponse(
    #         message=f"{otp_type} verified successfully",
    #         userId=user.id
    #     )
    

    # def invalidate_unused_otp(self,otp_type : str, user_id: int):
    #     otp_records = self.db.query(OTPCode).filter(
    #         and_(
    #             OTPCode.user_id == user_id,
    #             OTPCode.is_used == False,
    #             OTPCode.otp_type == otp_type,
    #             OTPCode.expires_at <= datetime.now()
    #         )
    #         ).all()
        
    #     for otp in otp_records:
    #         otp.is_used = True
    #         otp.updated_at = datetime.now()
    #     self.db.commit()


    # @staticmethod  
    # def check_otp_validity(otp):
    #     if len(otp) != 6:
    #         raise HTTPException(status_code=400, detail="OTP must be 6 digits long.")
        
    #     if not otp.isdigit():
    #         raise HTTPException(status_code=400, detail="OTP must contain only numbers.")
    
    
def get_otp_service(
        db: Session = Depends(get_db),
        # communication_service: CommunicationService = Depends(get_communication_service)
        ) -> OTPService:
    return OTPService(db)
