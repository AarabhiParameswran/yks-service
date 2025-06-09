import os
import shutil
from app.database import get_db
from app.models.file_upload import FileUpload
from app.schema.member import FamilyRelationBase
from app.service.master_services.jilla_service import JillaService, get_jilla_service
from app.service.master_services.member_service import MemberService, get_member_service
from fastapi import APIRouter, Depends
from app.service.master_services.token_service import oauth2_scheme
from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, File, Depends, Header
from tkinter.tix import Form

router = APIRouter(prefix="/member", tags=["Member API"])


@router.get("/member-details/{member_id}")
def get_member_details(member_id: float,member_service: MemberService = Depends(get_member_service),
                  token: str = Depends(oauth2_scheme)):
    return member_service.get_member_details(member_id,token)

@router.get("/")
def get_member(member_service: MemberService = Depends(get_member_service),
                  token: str = Depends(oauth2_scheme)):
    return member_service.get_members(token)

@router.post("/add-family")
def add_family(family_realtion: FamilyRelationBase,member_service: MemberService = Depends(get_member_service),
                  token: str = Depends(oauth2_scheme)):
    return member_service.add_family(family_realtion,token)