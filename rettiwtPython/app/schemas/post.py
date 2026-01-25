from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserSummary

class PostBase(BaseModel):
    text:str

class PostOut(BaseModel):
    id: int
    text:str
    media: Optional[bytes]
    created_at: datetime
    user:UserSummary
    like_count: int

    class Config:
        orm_mode= True

class PostCreate(PostBase):
    pass