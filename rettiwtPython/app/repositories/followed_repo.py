from sqlalchemy.orm import Session
from app.models.followed import Followed

def is_following(db: Session, user_id: int, by_user: int) -> bool:
    return db.query(Followed).filter(Followed.user_id == user_id, Followed.by_user_id == by_user).first() is not None


def get_followed_users(db:Session, by_user: int):
    return db.query(Followed).filter(Followed.by_user_id == by_user).all()

def get_followers(db:Session, user_id:int):
    return db.query(Followed).filter(Followed.user_id == user_id).all()

