from app.database import get_db
from app.models.news import News
from app.service.master_services.token_service import TokenService, get_token_service
from app.service.master_services.user_service import UserService, get_user_service
from fastapi import Depends, HTTPException,UploadFile
from sqlalchemy.orm import Session

class NewsService:
    def __init__(self, db,user_service: UserService,token_service: TokenService):
        self.db = db
        self.user_service = user_service
        self.token_service = token_service

    def get_news_by_category(self,category,district_id,token):
        self.token_service.get_user_from_token(token)
        if district_id :
            news = self.db.query(News).filter(News.category == category,News.district_id == district_id).all()
        else:
            news = self.db.query(News).filter(News.category == category).all()
        return news

def get_news_service(
        db: Session = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        token_service: TokenService = Depends(get_token_service),
        ) -> NewsService:
    return NewsService(db,user_service,token_service)