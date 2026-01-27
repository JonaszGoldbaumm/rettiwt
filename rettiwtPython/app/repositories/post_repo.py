from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.post import Post
from app.models.like import Like
from app.models.followed import Followed
from app.models.comment import Comment

def get_global_feed(db: Session):
    """
    Returns the global feed of all posts with like and comment counts.

    :param db: Database session
    :type db: Session
    """
    return (
        db.query(
            Post,
            func.count(func.distinct(Like.post_id)).label("like_count"),
            func.count(func.distinct(Comment.id)).label("comment_count"),
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .outerjoin(Comment, Comment.post_id == Post.id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )


def get_posts_by_user(db: Session, user_id: int):
    """
    Returns all posts by a specific user with like and comment counts.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    """
    return (
        db.query(
            Post,
            func.count(func.distinct(Like.post_id)).label("like_count"),
            func.count(func.distinct(Comment.id)).label("comment_count"),
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .outerjoin(Comment, Comment.post_id == Post.id)
        .filter(Post.user_id == user_id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )


def get_posts_with_media(db: Session):
    """
    Returns all posts that contain media.

    :param db: Database session
    :type db: Session
    """
    return (
        db.query(
            Post,
            func.count(func.distinct(Like.post_id)).label("like_count"),
            func.count(func.distinct(Comment.id)).label("comment_count"),
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .outerjoin(Comment, Comment.post_id == Post.id)
        .filter(Post.media.isnot(None))
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )


def get_followed_feed(db: Session, current_user: int):
    """
    Returns the feed for a user based on followed accounts.

    :param db: Database session
    :type db: Session
    :param current_user: ID of the current user
    :type current_user: int
    """
    return (
        db.query(
            Post,
            func.count(func.distinct(Like.post_id)).label("like_count"),
            func.count(func.distinct(Comment.id)).label("comment_count"),
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .outerjoin(Comment, Comment.post_id == Post.id)
        .join(Followed, Followed.user_id == Post.user_id)
        .filter(Followed.by_user_id == current_user)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .all()
    )

def get_by_id(db:Session, post_id: int):
    """
    Fetches a post by its ID.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    """
    return db.query(Post).filter(Post.id == post_id).first()

def delete_by_id(db:Session, post_id:int):
    """
    Deletes a post by its ID.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    """
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()

    