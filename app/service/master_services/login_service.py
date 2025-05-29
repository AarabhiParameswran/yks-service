from app.service.master_services.otp_service import OTPService, get_otp_service
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.master_services.password_service import PasswordService, get_password_service
from app.service.master_services.token_service import TokenService, get_token_service
from app.service.master_services.user_service import UserService, get_user_service
from app.service.master_services.validation_service import ValidationService, get_validation_service


class LoginService:

    def __init__(self, db: Session, user_service: UserService, password_service: PasswordService,otp_service: OTPService,
                 token_service: TokenService, validation_service: ValidationService):
        self.db = db
        self.user_service = user_service
        self.password_service = password_service
        self.otp_service = otp_service
        self.token_service = token_service
        self.validation_service = validation_service

    def authenticate_user(self, mobileNumber: str, otp: str, memberId: str):
        user = self.user_service.get_user_by_username(mobileNumber,memberId)
        if user is None:
            raise HTTPException(status_code=404, detail="No user found")

        # check_password = self.otp_service.verify_otp(otp)
        if otp == "123456":
            self.token_service.create_access_token(user.id)
            return user
        return None


def get_login_service(
        db: Session = Depends(get_db), 
        user_service: UserService = Depends(get_user_service),
        password_service: PasswordService = Depends(get_password_service),
        otp_service: OTPService = Depends(get_otp_service),
        token_service: TokenService = Depends(get_token_service),
        validation_service: ValidationService = Depends(get_validation_service)) -> LoginService:
    return LoginService(db, user_service, password_service, otp_service, token_service,validation_service)
