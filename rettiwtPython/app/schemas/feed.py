from pydantic import BaseModel
from typing import List
from app.schemas.post import PostOut

class FeedResponse(BaseModel):
    posts: List[PostOut]