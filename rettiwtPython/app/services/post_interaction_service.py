from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.repositories import post_repo, comment_repo, like_repo, user_repo

def create_post(db:Session, user_id: int, text: str, media: bytes | None):
    """
    Creates a new post for a user.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the authoring user
    :type user_id: int
    :param text: Post content text
    :type text: str
    :param media: Optional media bytes
    :type media: bytes | None
    :raises ValueError: If user does not exist
    """
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    post = Post(text=text, media=media, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db:Session, post_id:int):
    """
    Deletes a post by its ID.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    """
    post_repo.delete_by_id(db, post_id)

def like_post(db:Session, post_id: int, user_id:int):
    """
    Adds a like to a post by a user.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    :param user_id: ID of the liking user
    :type user_id: int
    :raises ValueError: If post or user does not exist
    """
    if like_repo.exists_by_post_and_user(db, post_id, user_id):
        return
    
    post=post_repo.get_by_id(db, post_id)
    if not post:
        raise ValueError("Post not found")
    
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    like = Like(post_id=post_id, user_id=user_id)
    like_repo.create_like(db, like)

def unlike_post(db:Session, post_id: int, user_id: int):
    """
    Removes a like from a post by a user.

    :param db: Database session
    :type db: Session
    :param post_id: ID of the post
    :type post_id: int
    :param user_id: ID of the user
    :type user_id: int
    """
    if not like_repo.exists_by_post_and_user(db, post_id, user_id):
        return
    
    like_repo.delete_by_post_and_user(db, post_id, user_id)

def create_comment(db:Session, user_id:int, post_id:int, text:str):
    """
    Creates a comment on a post.

    :param db: Database session
    :type db: Session
    :param user_id: ID of the commenting user
    :type user_id: int
    :param post_id: ID of the post
    :type post_id: int
    :param text: Comment text
    :type text: str
    :raises ValueError: If user or post does not exist
    """
    post= post_repo.get_by_id(db, post_id)
    if not post:
        raise ValueError("Post not found")
    
    user= user_repo.get_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    comment = Comment(text=text, post_id=post_id,user_id= user_id)
    comment_repo.create_comment(db, comment)

def delete_comment(db:Session, comment_id: int):
    """
    Deletes a comment by its ID.

    :param db: Database session
    :type db: Session
    :param comment_id: ID of the comment
    :type comment_id: int
    """
    comment_repo.delete_by_id(db, comment_id)

