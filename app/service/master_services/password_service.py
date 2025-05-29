import re
from passlib.context import CryptContext
from app.schema.user import PasswordPolicySettings
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    def __init__(self, 
                 db):
        self.db = db

    @staticmethod
    def check_password_policy(password: str) -> dict:
        errors = []
        policy = PasswordPolicySettings()

        # Check length
        if len(password) < policy.min_length:
            errors.append(f"Password must be at least {policy.min_length} characters long.")
        if len(password) > policy.max_length:
            errors.append(f"Password must be no more than {policy.max_length} characters long.")

        # Check for uppercase
        if policy.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")

        # Check for numbers
        if policy.require_number and not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number.")

        # Check for special characters
        if policy.require_special_char and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character from these 's!@#$%^&*(),.?”:{}|<>[]1E'")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return bcrypt_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt_context.verify(plain_password, hashed_password)


def get_password_service(
        db: Session = Depends(get_db)) -> PasswordService:
    return PasswordService(db)
