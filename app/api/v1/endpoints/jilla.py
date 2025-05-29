import os
import shutil
from app.database import get_db
from app.models.file_upload import FileUpload
from app.service.master_services.jilla_service import JillaService, get_jilla_service
from fastapi import APIRouter, Depends
from app.service.master_services.token_service import oauth2_scheme
from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, File, Depends, Header
from tkinter.tix import Form

router = APIRouter(prefix="/state", tags=["State API"])


@router.get("/jilla")
def get_jilla(jilla_service: JillaService = Depends(get_jilla_service),
                  token: str = Depends(oauth2_scheme)):
    return jilla_service.get_jilla(token)

@router.get("/upasabha/{district_code}")
def get_upasabha(district_code: int, jilla_service: JillaService = Depends(get_jilla_service),
                  token: str = Depends(oauth2_scheme)):
    return jilla_service.get_upasabha(district_code,token)


@router.post("/upload/")
def upload_file(upasabha_code: int, file: UploadFile = File(...), jilla_service: JillaService = Depends(get_jilla_service), token: str = Depends(oauth2_scheme)):
    return jilla_service.upload_file(token,upasabha_code,file)


@router.get("/upasabha/files/{upasabha_code}")
def get_files(upasabha_code: int, jilla_service: JillaService = Depends(get_jilla_service),
                  token: str = Depends(oauth2_scheme)):
    return jilla_service.get_upasabha_file(upasabha_code,token)