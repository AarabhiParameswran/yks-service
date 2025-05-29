from datetime import datetime
import os
import shutil
from app.database import get_db
from app.models.file_upload import FileUpload
from app.models.upasabha import Upasabha
from app.service.master_services.token_service import TokenService, get_token_service
from app.service.master_services.user_service import UserService, get_user_service
from fastapi import Depends, HTTPException,UploadFile
from sqlalchemy.orm import Session
from app.models.jilla import Jilla
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class JillaService:
    def __init__(self, db,user_service: UserService,token_service: TokenService):
        self.db = db
        self.user_service = user_service
        self.token_service = token_service

    def get_jilla(self,token):
        self.token_service.get_user_from_token(token)
        return self.db.query(Jilla).all()

    def get_upasabha(self, district_code: int, token: str):
        self.token_service.get_user_from_token(token)
        records = self.db.query(Upasabha).filter(Upasabha.district_code == district_code).all()
        return records
    
    def get_upasabha_file(self,upasabha_code :int ,token:str):
        self.token_service.get_user_from_token(token)
        records = self.db.query(FileUpload).filter(FileUpload.upasabha_code == upasabha_code).all()
        return records
    
    def upload_file(self, token: str, upasabha_code: int, file: UploadFile):
        user = self.token_service.get_user_from_token(token)

        extension = os.path.splitext(file.filename)[1]

        existing_files = (
            self.db.query(FileUpload)
            .filter_by(upasabha_code=upasabha_code)
            .order_by(FileUpload.pic_number)
            .all()
        )

        if len(existing_files) < 5:
            next_pic = len(existing_files) + 1
            filename = f"Pic_{upasabha_code}_{next_pic}{extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            file_url = f"/{UPLOAD_DIR}/{filename}"
            new_entry = FileUpload(
                upasabha_code=upasabha_code,
                file_url=file_url,
                pic_number=next_pic,
                created_at = datetime.now(),
                created_by = user.id
            )
            self.db.add(new_entry)
            self.db.commit()
            return {"message": f"File uploaded as Pic_{next_pic}", "url": file_url}

        else:

            existing_pics = {f.pic_number for f in existing_files}
            if len(existing_pics) != 5:
                raise ValueError("Unexpected state: less than 5 distinct pic numbers exist.")

            last_updated_pic = (
                self.db.query(FileUpload)
                .filter_by(upasabha_code=upasabha_code)
                .order_by(FileUpload.id.desc())  
                .first()
            )

            last_pic_number = last_updated_pic.pic_number
            next_pic = (last_pic_number % 5) + 1  

            file_to_overwrite = (
                self.db.query(FileUpload)
                .filter_by(upasabha_code=upasabha_code, pic_number=next_pic)
                .first()
            )

            filename = f"Pic_{upasabha_code}_{next_pic}{extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            file_url = f"/{UPLOAD_DIR}/{filename}"

            file_to_overwrite.file_url = file_url
            file_to_overwrite.pic_number = next_pic 
            file_to_overwrite.updated_at = datetime.now()
            file_to_overwrite.updated_by = user.id
            self.db.commit()

            return {"message": f"File overwritten as Pic_{next_pic}", "url": file_url}

    
def get_jilla_service(
        db: Session = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        token_service: UserService = Depends(get_token_service),
        ) -> JillaService:
    return JillaService(db,user_service,token_service)