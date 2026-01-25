from pydantic import BaseModel
from datetime import datetime

class UserSummary(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class UserPublic(BaseModel):
    id:int
    username:str
    email: str | None = None
    profile_pic: bytes | None = None
    description: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True

        