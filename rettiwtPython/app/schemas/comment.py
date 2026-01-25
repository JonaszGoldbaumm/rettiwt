from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserSummary

class CommentOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    user: UserSummary

    class Config:
        orm_mode=True

