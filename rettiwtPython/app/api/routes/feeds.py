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

def serialize_feed(rows):
    return [
        {
            "id": post.id,
            "text": post.text,
            "media": post.media,
            "created_at": post.created_at,
            "user": post.user,
            "like_count": like_count,
        }
        for post, like_count in rows
    ]

@router.get("/", response_model=FeedResponse)
def global_feed(db: Session = Depends(get_db)):
    posts = post_service.get_feed(db)
    return {"posts": serialize_feed(posts)}

@router.get("/user/{user_id}", response_model=FeedResponse)
def user_posts_feed(user_id: int, db: Session = Depends(get_db)):
    posts = post_service.get_user_feed(db, user_id)
    return {"posts": serialize_feed(posts)}

@router.get("/media", response_model=FeedResponse)
def media_feed(current_user: UserSummary = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = post_service.get_media_feed(db)
    return {"posts": serialize_feed(posts)}

@router.get("/followed", response_model=FeedResponse)
def followed_feed(current_user: UserSummary = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = post_service.get_followed_feed(db, current_user.id)
    return {"posts": serialize_feed(posts)}