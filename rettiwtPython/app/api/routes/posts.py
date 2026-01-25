from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.post import PostCreate, PostOut
from app.schemas.interaction import PostDetailsOut, CommentCreate, LikeActionOut
from app.services import post_details_service, post_interaction_service
from app.repositories import post_repo, comment_repo

router = APIRouter(prefix="/post", tags=["post"])

@router.post("/", response_model=PostOut)
async def create_post(
    text: str,
    media: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    curr_user=Depends(get_current_user),
):
    media_bytes: bytes | None = None
    if media:
        if media.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Invalid image type")
        media_bytes = await media.read()
    post = post_interaction_service.create_post(db, user_id=curr_user.id, text=text, media=media_bytes)
    return post

@router.get("/{post_id}", response_model=PostDetailsOut)
def get_post_details(post_id:int, db:Session = Depends(get_db), curr_user = Depends(get_current_user)):
    curr_user_id = curr_user.id if curr_user else None

    details = post_details_service.get_post_details(db, post_id, curr_user_id)
    if not details:
        raise HTTPException(status_code=404, detail="Post not found")
    return details

@router.post("/{post_id}/like", response_model=LikeActionOut)
def toggle_like(post_id:int, db:Session = Depends(get_db), curr_user = Depends(get_current_user)):
    from app.repositories.like_repo import exists_by_post_and_user

    if exists_by_post_and_user(db, post_id, curr_user.id):
        post_interaction_service.unlike_post(db, post_id, curr_user.id)
        return {"success":True}
    else:
        post_interaction_service.like_post(db, post_id, curr_user.id)
        return {"success":True}
    
@router.post("/{post_id}/comment")
def add_comment(post_id, data:CommentCreate, db:Session = Depends(get_db), curr_user = Depends(get_current_user)):
    post_interaction_service.create_comment(db, user_id=curr_user.id, post_id=post_id, text=data.text)
    return {"success":True}

@router.delete("/{post_id}")
def delete_post(post_id:int, db:Session = Depends(get_db), curr_user=Depends(get_current_user)):
    post= post_repo.get_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    post_interaction_service.delete_post(db, post_id)
    return {"success":True}

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id:int, db:Session= Depends(get_db), curr_user = Depends(get_current_user)):
    comment = comment_repo.get_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    post_interaction_service.delete_comment(db, comment_id)
    return {"success": True}
