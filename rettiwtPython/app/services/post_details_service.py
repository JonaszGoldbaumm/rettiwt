from sqlalchemy.orm import Session
from app.repositories import comment_repo, like_repo

def get_post_details(db:Session, post_id: int, curr_user:int | None):
    comments= comment_repo.get_by_post_with_user(db, post_id)
    likecnt= like_repo.count_by_post(db, post_id)

    liked = False
    if curr_user is not None:
        liked = like_repo.exists_by_post_and_user(db, post_id, curr_user)

    return {
        "post_id": post_id,
        "like_count": likecnt, 
        "liked_by_user": liked,
        "comments": comments
    }
