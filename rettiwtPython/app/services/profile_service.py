from sqlalchemy.orm import Session
from app.repositories import user_repo, followed_repo

def get_user_profile(db:Session, user_id:int):
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    follower_links = followed_repo.get_followers(db, user_id)
    followed_links = followed_repo.get_followed_users(db, user_id)

    followercnt = len(follower_links)
    followedcnt = len(followed_links)

    followers = [
        {"id": f.followed_by.id, "username": f.followed_by.username}
        for f in follower_links
    ]

    followed = [
        {"id": f.user.id, "username": f.user.username}
        for f in followed_links
    ]

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_pic": user.profile_pic,
        "description": user.description,
        "followers_count": followercnt,
        "followed_count": followedcnt,
        "followers": followers,
        "followed": followed,
    }