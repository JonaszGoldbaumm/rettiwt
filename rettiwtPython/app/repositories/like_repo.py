from sqlalchemy.orm import Session
from app.models.like import Like

def count_by_post(db:Session, post_id: int) -> int:
    """
    Counts the number of likes for a given post.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    :return: Number of likes
    :rtype: int
    """
    return db.query(Like).filter(Like.post_id == post_id).count()

def exists_by_post_and_user(db:Session, post_id:int, user_id:int) -> bool:
    """
    Checks if a user has liked a specific post.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    :param user_id: ID of the user
    :type user_id: int
    :return: True if the like exists, False otherwise
    :rtype: bool
    """
    return (db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first() is not None)

def create_like(db:Session, like: Like):
    """
    Creates a like record in the database.

    :param db: Database session
    :type db: Session
    :param like: Like object to persist
    :type like: Like
    """
    db.add(like)
    db.commit()

def delete_by_post_and_user(db:Session, post_id:int, user_id:int):
    """
    Deletes a like by matching post and user IDs.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    :param user_id: ID of the user
    :type user_id: int
    """
    db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).delete()
    db.commit()

    