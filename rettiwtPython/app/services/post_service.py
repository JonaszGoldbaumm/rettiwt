from sqlalchemy.orm import Session
from app.repositories import post_repo, followed_repo


def get_feed(db:Session):
    """
    Returns the global feed.

    :param db: Database session
    :type db: Session
    """
    return post_repo.get_global_feed(db)

def get_user_feed(db:Session, user_id:int):
    """
    Returns the feed for a specific user.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user
    :type user_id: int
    """
    return post_repo.get_posts_by_user(db, user_id)

def get_media_feed(db:Session):
    """
    Returns the feed of posts containing media.

    :param db: Database session
    :type db: Session
    """
    return post_repo.get_posts_with_media(db)

def get_followed_feed(db:Session, curr_user:int):
    """
    Returns the feed from followed users.

    :param db: Database session
    :type db: Session
    :param curr_user: ID of the current user
    :type curr_user: int
    """
    return post_repo.get_followed_feed(db, curr_user)

