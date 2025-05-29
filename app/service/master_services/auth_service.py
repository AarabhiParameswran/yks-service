from datetime import timedelta

from app.models.roles import Roles
from app.models.user_roles import UserRoles
from app.models.users import User
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from app.database import get_db
from app.service.master_services.login_service import LoginService, get_login_service
from app.service.master_services.token_service import TokenService, get_token_service

ACCESS_TOKEN_EXPIRE_MINUTES = 2
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_SECRET = "e2b7f6b2d334bf1a03eec8d4eb8e4d80f5b35621c2f3a7418d12b62e438d49c1"
REFRESH_SECRET = "e2b7f6b2d334bf1a03eec8d4eb8e4d80f5b35621c2f3a7418d12b62e438d49c1"
ALGORITHM = "HS256"


class AuthService:
    def __init__(self, db,
                 login_service: LoginService,
                 token_service: TokenService):
        self.db = db
        self.login_service = login_service
        self.token_service = token_service

    def login(self, user):
        user = self.login_service.authenticate_user(user.mobileNumber, user.otp,user.memberId)
        if user:
            access_token = self.token_service.create_access_token(user.id)
            refresh_token = self.token_service.create_refresh_token(user.id)

            roles = (
                self.db.query(Roles.role_name)
                .join(UserRoles, UserRoles.role_id == Roles.id)
                .join(User, UserRoles.user_id == User.id)
                .filter(User.id == user.id)
                .all()
            )

            role_list = [
                {"name": role.role_name}
                for role in roles
            ]

            role_names = [r.role_name for r in roles]
            required_roles = {"Member Role", "Upsabha Role","Jilla Role","State Role"}
            if not any(role in required_roles for role in role_names):
                raise HTTPException(status_code=403, detail="Access denied")

            result = {
                "accessToken": access_token,
                "tokenType": "bearer",
                "expiresIn": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": {
                    "id": user.id,
                    "firstName": user.user_name,
                    "lastName": user.mobile,
                    "roles": role_list
                }
            }
            response = JSONResponse(content=result)
            response.set_cookie(key="refresh_token", value=refresh_token)

            return response

        else:
            raise HTTPException(status_code=401, detail="Invalid username or otp expired")

    def get_refresh_token(self, refresh_token):
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        try:
            user_id = self.token_service.decode_token(refresh_token, REFRESH_SECRET)
        except HTTPException:
            raise

        user = self.db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = self.token_service.create_access_token(user_id)
        return {"accessToken": access_token}


def get_auth_service(
        db: Session = Depends(get_db),
        login_service: Session = Depends(get_login_service),
        token_service: Session = Depends(get_token_service)) -> AuthService:
    return AuthService(db, login_service, token_service)
