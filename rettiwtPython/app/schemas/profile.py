from pydantic import BaseModel
from typing import List, Optional
from app.schemas.user import UserSummary

class UserProfileOut(BaseModel):
    """
    Schema of user details used mainly for displaying profile information.
    Contains two extra fields of follower/followed counts and their respective lists.
    """
    id:int
    username:str
    email:Optional[str]
    description:Optional[str]

    followers_count:int
    followed_count:int

    followers: List[UserSummary]
    followed: List[UserSummary]