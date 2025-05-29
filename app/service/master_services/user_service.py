from typing import Optional
from fastapi import Depends, HTTPException
from app.database import get_db
from passlib.context import CryptContext
from app.models.roles import Roles
from app.models.users import User
from sqlalchemy.orm import Session
from app.models.user_roles import UserRoles
from app.schema.user import ChangePassword, UserCreate, UserUpdate
from app.service.master_services.password_service import PasswordService, get_password_service
from app.service.master_services.token_service import USER_NOT_FOUND_ERROR, TokenService, get_token_service
from app.service.master_services.validation_service import ValidationService, get_validation_service

class UserService:
    def __init__(self, 
                 db: Session,
                 password_service : PasswordService,
                 validation_service : ValidationService,
                 token_service: TokenService
                 ):
        self.db = db
        self.password_service = password_service
        self.validation_service = validation_service
        self.token_service = token_service
        
    def get_not_mapped_roles(self, user_id, token):
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)

        mapped_role_ids = self.db.query(UserRole.role_id).filter(UserRole.user_id == user_id)

        roles = self.db.query(Role).filter(~Role.id.in_(mapped_role_ids)).all()
        
        return roles


    def get_all_users(self, userfilter, token):
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        query = self.db.query(User).order_by(User.is_enabled.desc())
        roles = self.get_user_roles_by_id(user.id,token)

        user_name = userfilter.filters.user_name
        first_name =  userfilter.filters.first_name
        last_name =  userfilter.filters.last_name
        email =  userfilter.filters.email
        mobile_number =  userfilter.filters.mobile_number
        is_enabled =  userfilter.filters.is_enabled
        skip = userfilter.skip or 0
        limit = userfilter.limit or 0
        sort_fields = userfilter.sort


        if user_name:
            query = query.filter(User.user_name.ilike(f"%{user_name}%"))
        if first_name:
            query = query.filter(User.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(User.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if mobile_number:
            query = query.filter(User.mobile_number.ilike(f"%{mobile_number}%"))
        if is_enabled:
            query = query.filter(User.is_enabled == is_enabled)

        allowed_sort_fields = {"user_name", "first_name", "last_name", "email_id","is_enabled"}
        allowed_sort_order = {"asc", "desc"}   

        sort_criteria = []
        sort_criteria.append(User.is_enabled.desc())
        sort_criteria.append(User.user_name.asc())
        

        if sort_fields:
            for sort in sort_fields:
                if sort.field not in allowed_sort_fields:
                    raise HTTPException(status_code=400, detail="Invalid sort field")
                if sort.order not in allowed_sort_order:
                    raise HTTPException(status_code=400, detail="Invalid sort order")

                if sort.order == "asc":
                    query = query.order_by(getattr(User, sort.field).asc())
                if sort.order == "desc":
                    query = query.order_by(getattr(User, sort.field).desc())


        query = query.order_by(*sort_criteria)
        
        total = query.count()
        if limit != 0:
            users = query.offset(skip).limit(limit).all()
        else:
            users = query.all()
        db_total = self.db.query(User).count()

        user_with_roles = []
        for row in users:
            user_roles = self.get_user_roles_by_id(row.id, token) 
            user_data = {
                "id": row.id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "user_name": row.user_name,
                "mobile_number": row.mobile_number,
                "email": row.email,
                "is_enabled": row.is_enabled,
                "roles": user_roles  
            }
            user_with_roles.append(user_data)



        return {
            "db_total": db_total,
            "total": total,
            "users": user_with_roles
        }


    def get_user_by_id(self, user_id: str, token) -> Optional[User]:
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        user =  self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"message":"User not found"}
        else:
            return user

    def create_user(self, user: UserCreate,token) -> User:
        token_user = self.token_service.get_user_from_token(token)
        if not token_user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        username = self.db.query(User).filter(User.user_name == user.user_name).first()
        if username:
            raise HTTPException(status_code=400, detail={"message":"User name already exists","field":"user_name"})
        
        if user.email:
            self.validation_service.check_email_validity(user.email)
        
        if user.mobile_number:
            self.validation_service.check_mobile_validity(user.mobile_number)

        validation_result = self.password_service.check_password_policy(user.password)
        if not validation_result['is_valid']:
            raise HTTPException(status_code=400, detail=validation_result["errors"])

        hashed_password = self.password_service.hash_password(user.password)
    
        new_user = User(
            first_name = user.first_name,
            last_name = user.last_name,
            user_name = user.user_name,
            mobile_number = user.mobile_number,
            email = user.email,
            password_hash = hashed_password,
            is_enabled = True,
            created_by = token_user.id
        )
        self.db.add(new_user)
        self.db.commit()
        if user.roles:
            for role in user.roles:
                new_role = UserRoles(
                    user_id = new_user.id,
                    role_id = role,
                    created_by = token_user.id
                )
                self.db.add(new_role)
                self.db.commit()
        return {"message" : "User created"}
    
    def update_user(self, update: UserUpdate, token) -> User:
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        update_user = self.db.query(User).filter(
            User.id == update.id).first()
        if not update_user:
            raise HTTPException(status_code=404, detail="User not found")

        username = self.db.query(User).filter(User.user_name == update.user_name).where(User.id!=update.id).first()
        if username:
            raise HTTPException(status_code=400, detail={"message":"User name already exists","field":"user_name"})
        
        if update.email:
            self.validation_service.check_email_validity(update.email)
        
        if update.mobile_number:
            self.validation_service.check_mobile_validity(update.mobile_number)
 
        print("update_user",update_user.password_hash)

        update_user.first_name = update.first_name,
        update_user.last_name = update.last_name,
        update_user.user_name = update.user_name,
        update_user.mobile_number = update.mobile_number,
        update_user.email = update.email,
        update_user.is_enabled = update.is_enabled
        update_user.updated_by = user.id
        
        self.db.commit()
        if update.roles:
            for role in update.roles:
                exist_deity_map = self.db.query(UserRoles).filter(UserRoles.role_id == role,UserRoles.user_id == update_user.id).first()
                if exist_deity_map:
                    pass
                else:
                    new_map = UserRoles(
                      role_id = role,
                    user_id = update_user.id,
                    created_by = user.id
                    )
                    self.db.add(new_map)
                    self.db.commit()
        return {"message" : "User updated"}

    def delete_user(self, id : int, token):
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        delete_user = self.db.query(User).filter(
            User.id == id).first()

        if not delete_user:
            raise HTTPException(status_code=404, detail="User not found")

        delete_user.is_enabled = False
        self.db.commit()
        return {"message":"User deleted"}
    
    def get_user_roles_by_id(self, id, token):
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        roles = (self.db.query(UserRoles.id, Roles.id, Roles.role_name)
        .outerjoin(Roles, Roles.id == UserRoles.role_id)
        .filter(UserRoles.user_id == id)
        .all()
        )
        return [
            {
                "id": row[0],  # UserRole.id
                "role_id": row[1],  # Role.id
                "role_name": row[2],  # Role.roles_name
                "description": row[3]  # Role.description
            }
            for row in roles
        ] if roles else []


    def get_user_by_mobile(self, mobile_number: str) -> Optional[User]:
        user = self.db.query(User).filter(User.mobile_number == mobile_number).first()
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self.db.query(User).filter(User.email == email).first()
        return user
    
    def get_user_by_username(self, mobileNumber: str, memberId: str) -> Optional[User]:
        user = self.db.query(User).filter(User.mobile == mobileNumber,User.member_id == memberId).first()
        return user

    def update_change_password(self, password_data: ChangePassword, token):
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)

        user_to_update = self.db.query(User).filter(User.id == password_data.id).first()
        if not user_to_update:
            raise HTTPException(status_code=404, detail="DATA_NOT_FOUND_ERROR")

        validation_result = self.password_service.check_password_policy(password_data.new_password)
        if not validation_result['is_valid']:
            raise HTTPException(status_code=400, detail=validation_result["errors"])

        if self.password_service.verify_password(password_data.new_password, user_to_update.password_hash):
            raise HTTPException(status_code=400, detail="New password cannot be the same as the current password")

        hashed_password = self.password_service.hash_password(password_data.new_password)
        user_to_update.password_hash = hashed_password
        self.db.commit()

        return {
            "message": "Password updated successfully",
            "user_name": user_to_update.user_name,
            "password": password_data.new_password,
        }

        
    def reset_password(self,id,token):
        user = self.token_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_ERROR)
        
def get_user_service(
        db: Session = Depends(get_db),
        password_service: PasswordService = Depends(get_password_service),
        validation_service : ValidationService = Depends(get_validation_service),
        token_service: TokenService = Depends(get_token_service)) -> UserService:
    return UserService(db,password_service,validation_service,token_service)
