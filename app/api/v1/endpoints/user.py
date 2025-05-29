from fastapi import APIRouter, Depends
from app.schema.user import ChangePassword, UserCreate, UserFilter, UserUpdate
from app.service.master_services.user_service import UserService, get_user_service
from app.service.master_services.token_service import oauth2_scheme


router = APIRouter(tags=["User API"])


@router.get("/users/get-not-mapped-roles/{user_id}")
def get_not_mapped_roles(user_id, user_service: UserService = Depends(get_user_service),
                    token: str = Depends(oauth2_scheme)):
    return user_service.get_not_mapped_roles(user_id, token)

@router.post("/users/list")
def get_all_users(userfilter : UserFilter, user_service: UserService = Depends(get_user_service),
                  token: str = Depends(oauth2_scheme)):
    return user_service.get_all_users(userfilter, token)

@router.get("/users/{id}")
def get_user_by_id(id : int, user_service: UserService = Depends(get_user_service),
                   token: str = Depends(oauth2_scheme)):
    return user_service.get_user_by_id(id, token)


@router.get("/users/user-roles/{id}")
def get_user_roles_by_id(id: int, user_service: UserService = Depends(get_user_service),
                         token: str = Depends(oauth2_scheme)):
    return user_service.get_user_roles_by_id(id, token)

@router.post("/users/")
def create_user(create : UserCreate, user_service: UserService = Depends(get_user_service),
                token: str = Depends(oauth2_scheme)):
    return user_service.create_user(create,token)

@router.put("/users/")
def update_user(update : UserUpdate, user_service: UserService = Depends(get_user_service),
                token: str = Depends(oauth2_scheme)):
    return user_service.update_user(update, token)
    
@router.delete("/users/")
def delete_user(id : int, user_service: UserService = Depends(get_user_service),
                token: str = Depends(oauth2_scheme)):
    return user_service.delete_user(id, token)
    
    
