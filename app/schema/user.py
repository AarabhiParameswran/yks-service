from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    memberId: str
    mobileNumber : str
    otp : str


class UserCreate(BaseModel):
  user_name : str
  mobile_number : Optional[str] = None
  roles: Optional[List[int]]

class UserUpdate(BaseModel):
  id : int
  first_name : str
  last_name : str
  user_name : str
  email : Optional[str] = None
  mobile_number : Optional[str] = None
  is_enabled : bool
  roles: Optional[List[int]]

class ChangePassword(BaseModel):
  id: int
  new_password: str
 
class SortFieldBase(BaseModel):
    field : Optional[str] = None
    order : Optional[str] = None

class FilterFieldBase(BaseModel):
    user_name : Optional[str] = None
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[str] = None
    mobile_number : Optional[str] = None
    is_enabled : Optional[str] = None

class UserFilter(BaseModel):
    skip : Optional[int] = 0
    limit : Optional[int] = 10
    sort : Optional[List[SortFieldBase]] = None
    filters : Optional[FilterFieldBase] = None
   
   
  

  
class PasswordPolicySettings(BaseModel):
    min_length: int = 8
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_number: bool = True
    require_special_char: bool = True
    allow_previous_passwords: int = 5
    max_attempts: int = 5
    lockout_duration_minutes: int = 15
    password_expiry_days: int = 90