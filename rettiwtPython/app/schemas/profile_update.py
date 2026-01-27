from pydantic import BaseModel

class UsernameUpdate(BaseModel):
    """
    Schema used for username change requests.
    """
    new_username: str

class PasswordUpdate(BaseModel):
    """
    Schema used for password change requests.
    """
    new_password: str
    old_password: str

class DescriptionUpdate(BaseModel):
    """
    Schema used for description change requests. Description can be empty or null.
    """
    description: str | None = None


