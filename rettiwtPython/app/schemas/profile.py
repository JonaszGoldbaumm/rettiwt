from pydantic import BaseModel
from typing import List, Optional
from app.schemas.user import UserSummary

class UserProfileOut(BaseModel):
    id:int
    username:str
    email:Optional[str]
    profile_pic:Optional[bytes]
    description:Optional[str]

    followers_count:int
    followed_count:int

    followers: List[UserSummary]
    followed: List[UserSummary]