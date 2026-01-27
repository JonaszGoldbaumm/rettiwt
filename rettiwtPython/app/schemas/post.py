from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.schemas.comment import CommentOut
from app.schemas.user import UserSummary


class PostOut(BaseModel):
    """Schema with details of a post. Doesn't include comment list."""
    id: int
    text: str
    created_at: datetime
    user: UserSummary
    like_count: int
    comment_count: int

    class Config:
        orm_mode = True

class PostDetailsOut(BaseModel):
    """
    Schema for details of a post, including extra fields for like and comment counts.
    """
    post_id: int
    text: str
    created_at: datetime
    author: UserSummary
    like_count: int
    liked_by_user: bool
    comments: List[CommentOut]

    class Config:
        orm_mode = True