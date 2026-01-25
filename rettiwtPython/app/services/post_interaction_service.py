from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.repositories import post_repo, comment_repo, like_repo, user_repo

def create_post(db:Session, user_id: int, text: str, media: bytes | None):
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    post = Post(text=text, media=media, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db:Session, post_id:int):
    post_repo.delete_by_id(db, post_id)

def like_post(db:Session, post_id: int, user_id:int):
    if like_repo.exists_by_post_and_user(db, post_id, user_id):
        return
    
    post=post_repo.get_by_id(db, post_id)
    if not post:
        raise ValueError("Post not found")
    
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    like = Like(post_id, user_id)
    like_repo.create_like(db, like)

def unlike_post(db:Session, post_id: int, user_id: int):
    if not like_repo.exists_by_post_and_user(db, post_id, user_id):
        return
    
    like_repo.delete_by_post_and_user(db, post_id, user_id)

def create_comment(db:Session, user_id:int, post_id:int, text:str):
    post= post_repo.get_by_id(db, post_id)
    if not post:
        raise ValueError("Post not found")
    
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    comment = Comment(text, post_id, user_id)
    comment_repo.create_comment(db, comment)

def delete_comment(db:Session, comment_id: int):
    comment_repo.delete_by_id(db, comment_id)

