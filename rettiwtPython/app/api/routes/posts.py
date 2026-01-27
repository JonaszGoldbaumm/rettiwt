from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user, get_optional_user
from app.schemas.post import PostDetailsOut, PostOut
from app.schemas.interaction import CommentCreate, LikeActionOut
from app.schemas.user import UserSummary
from app.services import post_details_service, post_interaction_service
from app.repositories import post_repo, comment_repo
import imghdr

router = APIRouter(prefix="/post", tags=["post"])


@router.post("/", response_model=PostOut)
async def create_post(
    text: str = Form(...),
    media: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    curr_user:UserSummary=Depends(get_current_user),
):
    """
    Post creation endpoint
    
    :param text: Text content of the post
    :type text: str
    :param media: Optional photo with the post
    :type media: UploadFile | None
    :param db: Database session
    :type db: Session
    :param curr_user: Description
    """
    media_bytes: bytes | None = None
    if media:
        if media.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Invalid image type")
        media_bytes = await media.read()
    post = post_interaction_service.create_post(db, user_id=curr_user.id, text=text, media=media_bytes)
    post.like_count= 0
    post.comment_count=0
    return post

@router.get("/{post_id}", response_model=PostDetailsOut)
def get_post_details(post_id:int, db:Session = Depends(get_db), curr_user:UserSummary = Depends(get_optional_user)):
    """
    Specific posts details endpoint
    
    :param post_id: Posts id
    :type post_id: int
    :param db: Database session
    :type db: Session
    :param curr_user: Authentication
    """
    curr_user_id = curr_user.id if curr_user else None

    details = post_details_service.get_post_details(db, post_id, curr_user_id)
    if not details:
        raise HTTPException(status_code=404, detail="Post not found")
    return details

@router.get("/{post_id}/media")
def get_post_media(post_id: int, db: Session = Depends(get_db)):
    """
    Media of the post endpoint
    
    :param post_id: Posts id
    :type post_id: int
    :param db: Database session
    :type db: Session
    """
    post = post_repo.get_by_id(db, post_id)
    if not post or not post.media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    image_type = imghdr.what(None, h=post.media)
    if not image_type:
        raise HTTPException(status_code=400, detail="Invalid image data")

    return Response(content=post.media, media_type=f"image/{image_type}")

@router.post("/{post_id}/like", response_model=LikeActionOut)
def toggle_like(post_id:int, db:Session = Depends(get_db), curr_user:UserSummary = Depends(get_current_user)):
    """
    Liking/unliking the post endpoint.
    
    :param post_id: Posts id
    :type post_id: int
    :param db: Database session
    :type db: Session
    :param curr_user: Description
    """
    from app.repositories.like_repo import exists_by_post_and_user

    if exists_by_post_and_user(db, post_id, curr_user.id):
        post_interaction_service.unlike_post(db, post_id, curr_user.id)
        return {"success":True}
    else:
        post_interaction_service.like_post(db, post_id, curr_user.id)
        return {"success":True}
    
@router.post("/{post_id}/comment")
def add_comment(post_id, data:CommentCreate, db:Session = Depends(get_db), curr_user:UserSummary = Depends(get_current_user)):
    """
    Comment creation endpoint
    
    :param post_id: Posts id
    :param data: Description
    :type data: Request body of the comment
    :param db: Database session
    :type db: Session
    :param curr_user: Description
    """
    post_interaction_service.create_comment(db, user_id=curr_user.id, post_id=post_id, text=data.text)
    return {"success":True}

@router.delete("/{post_id}")
def delete_post(post_id:int, db:Session = Depends(get_db), curr_user:UserSummary=Depends(get_current_user)):
    """
    Post deletion endpoint
    
    :param post_id: Post id
    :type post_id: int
    :param db: Database session
    :type db: Session
    :param curr_user: Description
    """
    post= post_repo.get_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    post_interaction_service.delete_post(db, post_id)
    return {"success":True}

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id:int, db:Session= Depends(get_db), curr_user:UserSummary = Depends(get_current_user)):
    """
    Comment deletion endpoint
    
    :param comment_id: Comment id
    :type comment_id: int
    :param db: Database session
    :type db: Session
    :param curr_user: Description
    """
    comment = comment_repo.get_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    post_interaction_service.delete_comment(db, comment_id)
    return {"success": True}


