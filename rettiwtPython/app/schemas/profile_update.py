from pydantic import BaseModel

class UsernameUpdate(BaseModel):
    new_username: str

class PasswordUpdate(BaseModel):
    new_password: str
    old_password: str

class DescriptionUpdate(BaseModel):
    description: str | None = None

class ProfilePicUpdate(BaseModel):
    pass
