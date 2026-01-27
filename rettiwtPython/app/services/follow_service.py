from sqlalchemy.orm import Session
from app.repositories import followed_repo

def toggle_follow_user(db: Session, user_id: int, by_user: int) -> bool:
    """
    Toggles the follow state between two users.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user to follow/unfollow
    :type user_id: int
    :param by_user: ID of the user performing the action
    :type by_user: int
    :return: True if now following, False if unfollowed
    :rtype: bool
    """
    return followed_repo.toggle_follow(db, user_id, by_user)

def is_following(db:Session, user_id:int, curr_id:int)->bool:
    """
    Checks if one user is following another.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user being followed
    :type user_id: int
    :param curr_id: ID of the potential follower
    :type curr_id: int
    :return: True if curr_id follows user_id
    :rtype: bool
    """
    return followed_repo.is_following(db, user_id, curr_id)