from typing import Optional
from app.models.file_upload import FileUpload
from app.service.master_services.jilla_service import JillaService, get_jilla_service
from app.service.master_services.news_service import NewsService, get_news_service
from fastapi import APIRouter, Depends
from app.service.master_services.token_service import oauth2_scheme
from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, File, Depends, Header
from tkinter.tix import Form

router = APIRouter(prefix="/news", tags=["News API"])


@router.get("/get-news-by-category/")
def get_news_by_category(category: str, district_id: Optional[int] = None, news_service: NewsService = Depends(get_news_service),
                  token: str = Depends(oauth2_scheme)):
    return news_service.get_news_by_category(category,district_id,token)