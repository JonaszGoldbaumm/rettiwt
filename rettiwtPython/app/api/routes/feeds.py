from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services import post_service
from app.schemas.feed import FeedResponse
from app.schemas.post import PostOut
from app.schemas.user import UserSummary
from app.api.deps import get_current_user

router = APIRouter(prefix="/feed", tags=["feed"])

@router.get("/global", response_model=FeedResponse)
def global_feed(db: Session = Depends(get_db)):
    posts = post_service.get_feed(db)
    return {"posts": posts}

@router.get("/user/{user_id}", response_model=FeedResponse)
def user_posts_feed(user_id: int, db: Session = Depends(get_db)):
    posts = post_service.get_user_feed(db, user_id)
    return {"posts": posts}

@router.get("/media", response_model=FeedResponse)
def media_feed(current_user: UserSummary = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = post_service.get_media_feed(db)
    return {"posts": posts}

@router.get("/followed", response_model=FeedResponse)
def followed_feed(current_user: UserSummary = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = post_service.get_followed_feed(db, current_user.id)
    return {"posts": posts}