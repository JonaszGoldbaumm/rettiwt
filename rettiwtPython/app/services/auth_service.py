from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.models.user import User
from app.core.security import hash_passwd, verify_passwd, create_access_token

def register_user(db:Session, username: str, email:str, passwd:str):
    if user_repo.get_by_username(db,username):
        raise ValueError("Username already exists")
    if user_repo.get_by_email(db, email):
        raise ValueError("Email already exists")
    
    user = User(
        username= username,
        email= email,
        password = hash_passwd(passwd)
    )
    return user_repo.create_user(db, user)

def authenticate_user(db:Session, username_or_email: str, passwd: str):
    user = user_repo.get_by_username(db, username_or_email) or user_repo.get_by_email(db, username_or_email)

    if not user or not verify_passwd(passwd, user.password):
        return None
    
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }