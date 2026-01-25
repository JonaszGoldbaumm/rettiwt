from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.post import Post
from app.models.like import Like
from app.models.followed import Followed

def get_global_feed(db:Session):
    return (
        db.query(Post, func.count(Like.post_id).label("like_count")).outerjoin(Like, Like.post_id == Post.id).group_by(Post.id).order_by(Post.created_at.desc()).all()
    )

def get_posts_by_user(db:Session, user_id: int):
    return (
        db.query(
            Post,
            func.count(Like.post_id).label("like_count")
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .filter(Post.user_id == user_id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )

def get_posts_with_media(db:Session):
    return (
        db.query(
            Post,
            func.count(Like.post_id).label("like_count")
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .filter(Post.media.isnot(None))
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )

def get_followed_feed(db:Session, current_user: int):
    return (
        db.query(
            Post,
            func.count(Like.post_id).label("like_count")
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .join(Followed, Followed.user_id == Post.user_id)
        .filter(Followed.by_user_id == current_user)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )

def get_by_id(db:Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def delete_by_id(db:Session, post_id:int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()

    