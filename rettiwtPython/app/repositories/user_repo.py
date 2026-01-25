from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_by_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def update_username(db: Session, user_id: int, new_username: str):
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.username = new_username
    db.commit()
    db.refresh(user)
    return user

def update_password(db: Session, user_id: int, new_password: str):
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.password = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return user


def update_profile_pic(db: Session, user_id: int, pic: bytes | None):
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.profile_pic = pic
    db.commit()
    db.refresh(user)
    return user


def update_description(db: Session, user_id: int, desc: str | None):
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.description = desc
    db.commit()
    db.refresh(user)
    return user