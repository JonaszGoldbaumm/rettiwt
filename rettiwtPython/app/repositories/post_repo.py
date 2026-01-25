from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.followed import Followed

def get_global_feed(db:Session):
    return db.query(Post).order_by(Post.created_at.desc()).all()

def get_posts_by_user(db:Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()

def get_posts_with_media(db:Session):
    return db.query(Post).filter(Post.media.isnot(None)).order_by(Post.created_at.desc()).all()

def get_followed_feed(db:Session, current_user: int):
    return db.query(Post).join(Followed, Followed.user_id == Post.user_id).filter(Followed.by_user_id == current_user).order_by(Post.created_at.desc()).all()

def get_by_id(db:Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def delete_by_id(db:Session, post_id:int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()

    