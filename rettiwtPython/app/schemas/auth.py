from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    """
    Schema used for user registration request.
    """
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Schema used for user login request.
    """
    username_or_email: str
    password: str
