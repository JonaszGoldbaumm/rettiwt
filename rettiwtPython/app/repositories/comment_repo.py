from sqlalchemy.orm import Session
from app.models.comment import Comment

def get_by_post_with_user(db:Session, post_id:int):
    """
    Returns all comments which match post id
    
    :param db: Database session
    :type db: Session
    :param post_id: Checked post id
    :type post_id: int
    """
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()

def create_comment(db:Session, comment:Comment):
    """
    Creates a comment record in db
    
    :param db: Database session
    :type db: Session
    :param comment: Comment object to create
    :type comment: Comment
    """
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def delete_by_id(db:Session, comment_id:int):
    """
    Deletes a comment by its matching id
    
    :param db: Database session
    :type db: Session
    :param comment_id: Id to match
    :type comment_id: int
    """
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()

def get_by_id(db:Session, comment_id: int):
    """
    Fetches a comment with id matching desired one 
    
    :param db: Database session
    :type db: Session
    :param comment_id: Id to match
    :type comment_id: int
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()

