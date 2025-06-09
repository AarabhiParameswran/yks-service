from typing import List, Optional
from pydantic import BaseModel, EmailStr

class FamilyRelationBase(BaseModel):
    memberId: float
    familyMemberId : float
    relation : str