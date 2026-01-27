from pydantic import BaseModel
from datetime import datetime

class UserSummary(BaseModel):
    """
    Schema used for displaying basic user information.
    """
    id: int
    username: str

    class Config:
        orm_mode = True

        