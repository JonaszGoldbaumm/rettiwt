from datetime import datetime
from pydantic import BaseModel
from typing import List
from app.schemas.comment import CommentOut
from app.schemas.user import UserSummary




class LikeActionOut(BaseModel):
    """
    Schema for the liking response(if it's a success or not)
    """
    success:bool

class CommentCreate(BaseModel):
    """
    Schema for comment creation request.
    """
    text:str