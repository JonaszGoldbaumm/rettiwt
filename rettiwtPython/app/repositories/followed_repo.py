from sqlalchemy.orm import Session
from app.models.followed import Followed

def is_following(db: Session, user_id: int, by_user: int) -> bool:
    """
    Checks whether a user is following another user.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user being followed
    :type user_id: int
    :param by_user: ID of the user who may be following
    :type by_user: int
    :return: True if by_user follows user_id, False otherwise
    :rtype: bool
    """
    return db.query(Followed).filter(Followed.user_id == user_id, Followed.by_user_id == by_user).first() is not None


def get_followed_users(db:Session, by_user: int):
    """
    Returns all users followed by a given user.

    :param db: Database session
    :type db: Session
    :param by_user: ID of the user who follows others
    :type by_user: int
    """
    return db.query(Followed).filter(Followed.by_user_id == by_user).all()

def get_followers(db:Session, user_id:int):
    """
    Returns all followers of a given user.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user being followed
    :type user_id: int
    """
    return db.query(Followed).filter(Followed.user_id == user_id).all()

def toggle_follow(db: Session, user_id: int, by_user: int) -> bool:
    """
    Toggles the follow state between two users.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the user being followed/unfollowed
    :type user_id: int
    :param by_user: ID of the user performing the action
    :type by_user: int
    :return: True if now following, False if unfollowed
    :rtype: bool
    """
    follow = db.query(Followed).filter(Followed.user_id == user_id, Followed.by_user_id == by_user).first()
    if follow:
        db.delete(follow)
        db.commit()
        return False
    else:
        new_follow = Followed(user_id=user_id, by_user_id=by_user)
        db.add(new_follow)
        db.commit()
        return True