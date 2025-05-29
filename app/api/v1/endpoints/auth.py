from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.responses import JSONResponse
from app.schema.user import UserBase
from app.service.master_services.auth_service import AuthService, get_auth_service


router = APIRouter(tags=["Authorization API"])

@router.post("/login")
def login(user: UserBase, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(user)

@router.post("/refresh")
def get_refresh_token(refresh_token: str = Cookie(None), auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.get_refresh_token(refresh_token)

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}