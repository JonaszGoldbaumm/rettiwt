from pydantic import BaseModel
from typing import List
from app.schemas.post import PostOut

class FeedResponse(BaseModel):
    """
    Schema for feed responses. 
    """
    posts: List[PostOut]