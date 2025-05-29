from datetime import datetime, timedelta, UTC
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.roles import Roles
from app.models.users import User
from app.models.user_roles import UserRoles

USER_NOT_FOUND_ERROR = "User not found"

ACCESS_SECRET = "e2b7f6b2d334bf1a03eec8d4eb8e4d80f5b35621c2f3a7418d12b62e438d49c1"
REFRESH_SECRET = "e2b7f6b2d334bf1a03eec8d4eb8e4d80f5b35621c2f3a7418d12b62e438d49c1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS= 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenService:

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def create_jwt_token(data: dict, secret: str, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire, "iat": datetime.now(UTC)})
        return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

    def create_access_token(self, user_id: int):

        roles = (
            self.db.query(Roles.role_name)
            .join(UserRoles, UserRoles.role_id == Roles.id)
            .filter(UserRoles.user_id == user_id)
            .all()
        )
        token_data = {
            "sub": str(user_id),
            "roles": [role.role_name for role in roles]
        }
        return self.create_jwt_token(token_data, ACCESS_SECRET, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    def create_refresh_token(self, user_id: int):
        roles = (
            self.db.query(Roles.role_name)
            .join(UserRoles, UserRoles.role_id == Roles.id)
            .filter(UserRoles.user_id == user_id)
            .all()
        )
        token_data = {
            "sub": str(user_id),
            "roles": [role.role_name for role in roles]
        }
        return self.create_jwt_token(token_data, REFRESH_SECRET, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    @staticmethod
    def decode_token(token: str, secret: str):
        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
            return payload["sub"]
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    @staticmethod
    def verify_access_token(token: str) -> str:
        try:
            payload = jwt.decode(token, ACCESS_SECRET, algorithms=[ALGORITHM])
            return payload["sub"]
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    # def invalidate_unused_reset_tokens(self, user_id: int):
    #     reset_tokens = self.db.query(PasswordResetToken).filter(
    #         and_(
    #             PasswordResetToken.user_id == user_id,
    #             PasswordResetToken.is_used == False,
    #             PasswordResetToken.expires_at <= datetime.now()
    #         )
    #         ).all()

    #     for token in reset_tokens:
    #         token.is_used = True
    #         token.updated_at = datetime.now()

    #     self.db.commit()

    def get_user_from_token(self, token):
        user_id = self.verify_access_token(token)
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

def get_token_service(
        db: Session = Depends(get_db)) -> TokenService:
    return TokenService(db)
