from pydantic import BaseModel
from typing import List
from app.schemas.comment import CommentOut

class PostDetailsOut(BaseModel):
    post_id: int
    like_count: int
    liked_by_user: bool
    comments: List[CommentOut]

class LikeActionOut(BaseModel):
    success:bool

class CommentCreate(BaseModel):
    text:str