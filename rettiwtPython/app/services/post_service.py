from sqlalchemy.orm import Session
from app.repositories import post_repo, followed_repo

def get_feed(db:Session):
    return post_repo.get_global_feed(db)

def get_user_feed(db:Session, user_id:int):
    return post_repo.get_posts_by_user(db, user_id)

def get_media_feed(db:Session):
    return post_repo.get_posts_with_media(db)

def get_followed_feed(db:Session, curr_user:int):
    return post_repo.get_followed_feed(db, curr_user)

