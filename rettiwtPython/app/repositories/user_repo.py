from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def get_by_username(db: Session, username: str):
    """
    Fetches a user by username.

    :param db: Database session
    :type db: Session
    :param username: Username to match
    :type username: str
    """
    return db.query(User).filter(User.username == username).first()

def get_by_email(db: Session, email: str):
    """
    Fetches a user by email.

    :param db: Database session
    :type db: Session
    :param email: Email to match
    :type email: str
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    """
    Creates a new user record in the database.

    :param db: Database session
    :type db: Session
    :param user: User object to persist
    :type user: User
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_by_id(db:Session, user_id:int):
    """
    Fetches a user by ID.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    """
    return db.query(User).filter(User.id == user_id).first()

def update_username(db: Session, user_id: int, new_username: str):
    """
    Updates a user's username.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    :param new_username: New username value
    :type new_username: str
    """
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.username = new_username
    db.commit()
    db.refresh(user)
    return user

def update_password(db: Session, user_id: int, new_password: str):
    """
    Updates a user's password.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    :param new_password: New raw password (will be hashed)
    :type new_password: str
    """
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.password = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return user


def update_profile_pic(db: Session, user_id: int, pic: bytes | None):
    """
    Updates a user's profile picture.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    :param pic: New profile picture bytes or None
    :type pic: bytes | None
    """
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.profile_pic = pic
    db.commit()
    db.refresh(user)
    return user


def update_description(db: Session, user_id: int, desc: str | None):
    """
    Updates a user's profile description.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    :param desc: New description text or None
    :type desc: str | None
    """
    user = get_by_id(db, user_id)
    if not user:
        return None
    user.description = desc
    db.commit()
    db.refresh(user)
    return user