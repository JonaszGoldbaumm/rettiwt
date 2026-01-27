from sqlalchemy.orm import Session
from app.repositories import comment_repo, like_repo, post_repo

def get_post_details(db:Session, post_id: int, curr_user:int | None):
    """
    Returns detailed information about a post, including likes and comments.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    :param curr_user: ID of the current user (if logged in)
    :type curr_user: int | None
    :return: Dictionary with post details, author, likes, and comments
    :rtype: dict
    """
    comments= comment_repo.get_by_post_with_user(db, post_id)
    likecnt= like_repo.count_by_post(db, post_id)

    liked = False
    if curr_user is not None:
        liked = like_repo.exists_by_post_and_user(db, post_id, curr_user)


    post = post_repo.get_by_id(db, post_id)
    if not post:
        return None

    return {
        "post_id": post.id, # type: ignore
        "text": post.text, # type: ignore
        "created_at": post.created_at, # type: ignore
        "author": {
            "id": post.user.id, # type: ignore
            "username": post.user.username, # type: ignore
        },
        "like_count": likecnt,
        "liked_by_user": liked,
        "comments": comments,
    }
