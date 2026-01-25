from sqlalchemy.orm import Session
from app.models.like import Like

def count_by_post(db:Session, post_id: int) -> int:
    return db.query(Like).filter(Like.post_id == post_id).count()

def exists_by_post_and_user(db:Session, post_id:int, user_id:int) -> bool:
    return (db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first() is not None)

def create_like(db:Session, like: Like):
    db.add(like)
    db.commit()

def delete_by_post_and_user(db:Session, post_id:int, user_id:int):
    db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).delete()
    db.commit()

    