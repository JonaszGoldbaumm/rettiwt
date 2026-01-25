from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserSummary

class PostBase(BaseModel):
    text:str
    media: Optional[bytes]=None

class PostOut(BaseModel):
    id: int
    text:str
    media: Optional[bytes]
    created_at: datetime
    user:UserSummary

    class Config:
        orm_mode= True

class PostCreate(PostBase):
    pass