from app.database import get_db
from app.models.family_relation import FamilyRelation
from app.models.file_upload import FileUpload
from app.models.member import Members
from app.models.upasabha import Upasabha
from app.service.master_services.token_service import TokenService, get_token_service
from app.service.master_services.user_service import UserService, get_user_service
from fastapi import Depends, HTTPException,UploadFile
from sqlalchemy.orm import Session
from app.models.jilla import Jilla
from sqlalchemy.sql import func



class MemberService:
    def __init__(self, db,user_service: UserService,token_service: TokenService):
        self.db = db
        self.user_service = user_service
        self.token_service = token_service

    def get_member_details(self,member_id,token):
        self.token_service.get_user_from_token(token)
        member_details = self.db.query(Members).filter(Members.member_id == member_id).first()
        return member_details

    def get_members(self,token):
        self.token_service.get_user_from_token(token)
        members = self.db.query(Members).all()
        return members  
    
    def add_family(self,family_realtion,token):
        user = self.token_service.get_user_from_token(token)
        member_details = self.db.query(Members).filter(Members.member_id == family_realtion.memberId).first()
        if not member_details:
            raise HTTPException(status_code=404, detail="No Member found")
        family_member_details = self.db.query(Members).filter(Members.member_id == family_realtion.familyMemberId).first()
        if not family_member_details:
            raise HTTPException(status_code=404, detail="No Member found")
        
        if member_details.house == family_member_details.house:
            new_family = FamilyRelation(
                member_id = family_realtion.memberId,
                family_member_id = family_realtion.familyMemberId,
                relation = family_realtion.relation,
                created_by = user.id,
                created_at = func.now()
            )
            self.db.add(new_family)        
            self.db.commit()               
            self.db.refresh(new_family) 
            return {"message": "Family attached successfully"}
        else:
            raise HTTPException(status_code=400, detail="You cannot add a person not with same house name as a family")


def get_member_service(
        db: Session = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        token_service: UserService = Depends(get_token_service),
        ) -> MemberService:
    return MemberService(db,user_service,token_service)